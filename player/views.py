from django.views.generic import DeleteView, ListView, DetailView
from django.urls import reverse_lazy

from player.models import Player
from patern.models import PatternType


class PlayerList(ListView):
    model = Player
    paginate_by = 10
    template_name = 'player/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Игроки'
        return context


class PlayerDel(DeleteView):
    model = Player
    success_url = reverse_lazy('player:list')


class PlayerDetail(DetailView):
    model = Player
    template_name = 'player/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object
        context['keys'] = ['unknown',]
        currency_list = ['USD', 'EUR']
        detail = {}
        detail['tour'] = {}
        detail['unknown'] = {}
        for currency in currency_list:
            detail['tour'][currency] = self.get_tournaments(currency)
            detail['unknown'][currency] = self.get_unknown(currency)

        for item in PatternType.objects.exclude(pattern_name='Турниры'):
            detail[item.pattern_name] = {}
            context['keys'].append(item.pattern_name)
            for currency in currency_list:
                detail[item.pattern_name][currency] = self.get_patern(item.pattern_name, currency)

        for currency in currency_list:
            if detail['tour'][currency] is not None:
                count = detail['tour'][currency]['count']
                t_sum = detail['tour'][currency]['sum']
                abi = t_sum/count
                detail['tour'][currency]['abi'] = round(abi, 2) * -1
            else:
                continue

            if detail['Ребаи'][currency] is not None:
                r_sum = detail['Ребаи'][currency]['sum']
                t_sum = t_sum + r_sum
            detail['tour'][currency]['sum'] = round(t_sum, 2)

            if detail['Выплаты'][currency] is not None:
                pay_off = detail['Выплаты'][currency]['sum']
                profit = pay_off + t_sum
                detail['Выплаты'][currency]['sum'] = round(pay_off, 2)
            else:
                profit = t_sum
            detail['tour'][currency]['profit'] = round(profit, 2)
        context['detail'] = detail

        return context

    def get_tournaments(self, currency):
        tournaments = {}
        tour_counts = {'sum': 0, 'count': 0}
        queryset = self.object.audit.filter(action_type='Турниры',
                                            curency=currency)
        if len(queryset) < 1:
            return None
        for item in queryset:
            if item.summary not in tournaments.keys():
                tournaments[item.summary] = [item]
                tour_counts['sum'] += item.summary
                tour_counts['count'] += 1
            else:
                tournaments[item.summary].append(item)
                tour_counts['sum'] += item.summary
                tour_counts['count'] += 1
        # sorting keys of dict for tournament's queryset
        buf_dict = {}
        for key in sorted(tournaments.keys()):
            buf_dict[f'BI: {key} {currency}'] = tournaments[key]
        tournaments = buf_dict
        tournaments.update(tour_counts)
        return tournaments

    def get_patern(self, pattern, currency):
        container_dict = {'query': [], 'sum': 0}
        queryset = self.object.audit.filter(action_type=pattern,
                                            curency=currency)
        if len(queryset) < 1:
            return None
        for item in queryset:
            container_dict['query'].append(item)
            container_dict['sum'] += item.summary
        return container_dict

    def get_unknown(self, currency):
        container_dict = {'query': [], 'sum': 0}
        queryset = self.object.audit.filter(action_type='NAN', curency=currency)
        if len(queryset) < 1:
            return None
        for item in queryset:
            container_dict['query'].append(item)
            container_dict['sum'] += item.summary
        container_dict['sum'] = round(container_dict['sum'], 2)
        return container_dict
