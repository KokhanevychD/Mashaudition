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
        details = {}
        tournaments = {'sum': 0, 'abi': 0}
        for item in player.audit.all():
            if item.action_type == 'Турниры':
                if f'bi: {item.summary}' not in tournaments.keys():
                    tournaments[f'bi: {item.summary}'] = [item, ]
                    tournaments['sum'] += item.summary
                    tournaments['abi'] += 1
                else:
                    tournaments[f'bi: {item.summary}'].append(item)
                    tournaments['sum'] += item.summary
                    tournaments['abi'] += 1
                continue
            if item.action_type not in details.keys():
                details[item.action_type] = {}
                details[item.action_type]['queryset'] = [item]
                details[item.action_type]['sum'] = item.summary
            else:
                details[item.action_type]['queryset'].append(item)
                details[item.action_type]['sum'] += item.summary
            if not item.action_type:
                if len(details['Не распознано']['queryset']) < 1:
                    details['Не распознано']['queryset'] = [item]
                    details['Не распознано']['sum'] = item.summary
                else:
                    details['Не распознано']['queryset'].append(item)
                    details['Не распознано']['sum'] += item.summary
        tournaments['sum'] = round(tournaments['sum'], 2)
        tournaments['abi'] = round(-1*(tournaments['sum']/tournaments['abi']),
                                   2)
        tournaments['profit'] = tournaments['sum'] + details['Выплаты']['sum']
        details['Турниры'] = tournaments
        context['details'] = details
        return context
