from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import requests
from io import BytesIO

def download_club_players(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    players = club.members.filter(role='PLAYER').order_by('full_name')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{club.name}_players.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, f"{club.name} - Registered Players")

    y = height - 100

    for player in players:
        # Draw photo if available
        if player.profile_photo:
            try:
                img_url = player.profile_photo.url
                img_response = requests.get(img_url, timeout=5)
                if img_response.status_code == 200:
                    img = ImageReader(BytesIO(img_response.content))
                    p.drawImage(img, 50, y - 60, width=50, height=50, mask='auto')
            except Exception:
                pass

        # Player details
        p.setFont("Helvetica-Bold", 11)
        p.drawString(110, y - 20, player.full_name)
        p.setFont("Helvetica", 10)
        p.drawString(110, y - 35, player.get_position_display())

        y -= 70

        # New page if needed
        if y < 100:
            p.showPage()
            y = height - 50

    p.showPage()
    p.save()
    return response