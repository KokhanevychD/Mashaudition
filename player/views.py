from django.views.generic import DeleteView, ListView, DetailView
from django.urls import reverse_lazy

from player.models import Player


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
        player = Player.objects.get(pk=self.kwargs['pk'])
        context['title'] = player
        # data containers
        details = {}
        tournaments = {}
        tour_counts = {'sum': 0, 'count': 0}

        for item in player.audit.all():
            # tournament selection
            if item.action_type == 'Турниры':
                if  item.summary not in tournaments.keys():
                    tournaments[item.summary] = [item]
                    tour_counts['sum'] += item.summary
                    tour_counts['count'] += 1
                else:
                    tournaments[item.summary].append(item)
                    tour_counts['sum'] += item.summary
                    tour_counts['count'] += 1
                continue
            # other types
            if item.action_type not in details.keys():
                details[item.action_type] = {}
                details[item.action_type]['queryset'] = [item]
                details[item.action_type]['sum'] = item.summary
            else:
                details[item.action_type]['queryset'].append(item)
                details[item.action_type]['sum'] += item.summary
            # items with no action_type, for rework
            if item.action_type == '':
                if 'Unknown' not in details.keys():
                    details['Unknown'] = {}
                    details['Unknown']['queryset'] = [item]
                    details['Unknown']['sum'] = item.summary
                else:
                    details['Unknown']['queryset'].append(item)
                    details['Unknown']['sum'] += item.summary

        if 'Ребаи' in details.keys():
            rebuy = details['Ребаи']
            rebuy_count = details['Ребаи']['sum']
        else:
            rebuy = []
            rebuy_count = 0
        if tour_counts['sum'] > 0:
            tour_counts['sum'] = round(tour_counts['sum'], 2)
            trnmt_and_rebuy_count = tour_counts['count'] + len(rebuy)
            tour_counts['abi'] = -1 * (tour_counts['sum'] / trnmt_and_rebuy_count)
            tour_counts['abi'] = round(tour_counts['abi'])
        # sorting keys of dict for tournament's queryset
        buf_dict = {}
        for key in sorted(tournaments.keys()):
            buf_dict[f'bi: {key}'] = tournaments[key]
        tournaments = buf_dict
        # sum of known ingame money movement to find profit
        tour_counts['profit'] = tour_counts['sum'] + \
            details['Выплаты']['sum'] + rebuy_count

        tour_counts['profit'] = round(tour_counts['profit'], 2)
        tournaments.update(tour_counts)
        details['Турниры'] = tournaments
        context['details'] = details
        return context
