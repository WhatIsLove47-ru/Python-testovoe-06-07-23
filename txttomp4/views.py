from django.http import FileResponse
from django.core.files.temp import NamedTemporaryFile
from django.utils.text import slugify
from dbapp.models import Query
import moviepy.editor as mp
from trans import trans

def home_view(request):
    if request.method == 'GET':
        h, w = screensize = (100,100)
        duration = 3
        txt = request.GET.get('text', None)
        if txt is not None:
            q = Query.objects.create(query_text=txt)
            clip_txt = mp.TextClip(txt, color='white', font="Amiri-Bold", kerning = 5, fontsize=90)
            txt_speed = clip_txt.size[0] / duration
            fl = lambda gf,t : gf(t)[:,int(txt_speed*t):int(txt_speed*t)+w]
            moving_txt = clip_txt.fl(fl, apply_to=['mask'])
            clip = mp.CompositeVideoClip([moving_txt.set_pos(('center','center'))], size = screensize)
            newfile = NamedTemporaryFile(suffix='.mp4')
            clip.set_duration(duration).write_videofile(newfile.name, fps=25)
            response = FileResponse(open(newfile.name, 'rb'))
            response['Content-Disposition'] = f'attachment; filename={slugify(trans(txt))}.mp4'
            response['Access-Control-Expose-Headers'] = 'Content-Disposition'
            return response
        return null
    return null
