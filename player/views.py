from django.views.generic.list import ListView

from player.models import Player


class PlayerList(ListView):
    model = Player
    paginate_by = 10
    template_name = 'player/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Игроки'
        return context
