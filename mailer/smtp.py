import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

def score_color(score):
    if score >= 8: return "#4ade80"
    if score >= 6: return "#facc15"
    return "#f87171"

def score_label(score):
    if score >= 8: return "HIGH"
    if score >= 6: return "MED"
    return "LOW"

def type_color(t):
    if t == "Confirmed": return "#4ade80"
    if t == "Contract": return "#60a5fa"
    return "#a78bfa"

def send_transfer_email(to_email: str, team: str, analysis):
    login = os.getenv("BREVO_LOGIN")
    password = os.getenv("BREVO_PASSWORD")
    date_str = datetime.now().strftime("%B %d, %Y")

    if isinstance(analysis, dict) and "transfers" in analysis:
        transfers = analysis["transfers"]
        summary = analysis.get("summary", "")
        overall = analysis.get("overall_score", "N/A")

        rows = ""
        for i, t in enumerate(transfers):
            sc = t.get("score", 5)
            typ = t.get("type", "Rumour")
            rows += f"""
            <tr>
                <td style="padding:14px 0;border-bottom:1px solid #1a1a2e;">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                        <div>
                            <span style="color:#ffffff;font-weight:600;font-size:15px;">{t.get('player','')}</span>
                            <div style="margin-top:4px;color:#6b7280;font-size:13px;">
                                {t.get('from','?')} 
                                <span style="color:#a78bfa;margin:0 6px;">→</span> 
                                {t.get('to','?')}
                            </div>
                            <div style="margin-top:6px;color:#9ca3af;font-size:12px;line-height:1.5;">{t.get('detail','')}</div>
                        </div>
                        <div style="text-align:right;min-width:80px;padding-left:12px;">
                            <span style="
                                background:{type_color(typ)}22;
                                color:{type_color(typ)};
                                border:1px solid {type_color(typ)}44;
                                padding:2px 8px;
                                border-radius:999px;
                                font-size:10px;
                                font-weight:600;
                                letter-spacing:1px;
                                display:block;
                                margin-bottom:6px;
                            ">{typ.upper()}</span>
                            <span style="
                                background:{score_color(sc)}22;
                                color:{score_color(sc)};
                                border:1px solid {score_color(sc)}44;
                                padding:2px 8px;
                                border-radius:999px;
                                font-size:10px;
                                font-weight:700;
                                display:block;
                            ">{score_label(sc)} {sc}/10</span>
                        </div>
                    </div>
                </td>
            </tr>
            """

        html = f"""
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"></head>
<body style="margin:0;padding:0;background:#030308;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#030308;padding:40px 20px;">
<tr><td align="center">
<table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;">
  <tr>
    <td style="background:linear-gradient(135deg,#1a0533 0%,#0d1526 100%);border:1px solid #2d1b69;border-radius:16px 16px 0 0;padding:36px 40px;text-align:center;">
        <div style="display:inline-block;background:rgba(167,139,250,0.1);border:1px solid rgba(167,139,250,0.25);border-radius:999px;padding:4px 14px;font-size:10px;letter-spacing:3px;color:#a78bfa;text-transform:uppercase;margin-bottom:16px;">⚽ Transfer Intelligence</div>
        <div style="font-size:28px;font-weight:700;color:#ffffff;letter-spacing:-0.5px;">{team}</div>
        <div style="font-size:13px;color:#6b7280;margin-top:6px;">{date_str} · Top 10 Briefing</div>
    </td>
  </tr>
  <tr>
    <td style="background:#0d0d1a;border-left:1px solid #2d1b69;border-right:1px solid #2d1b69;padding:16px 40px;">
        <table width="100%" cellpadding="0" cellspacing="0">
        <tr>
            <td style="color:#6b7280;font-size:11px;letter-spacing:2px;text-transform:uppercase;">Overall Reliability</td>
            <td align="right">
                <span style="background:{score_color(overall)}22;color:{score_color(overall)};border:1px solid {score_color(overall)}44;padding:3px 12px;border-radius:999px;font-size:12px;font-weight:700;">{overall}/10</span>
            </td>
        </tr>
        </table>
    </td>
  </tr>
  <tr>
    <td style="background:#080810;border-left:1px solid #2d1b69;border-right:1px solid #2d1b69;padding:0 40px;">
        <table width="100%" cellpadding="0" cellspacing="0">{rows}</table>
    </td>
  </tr>
  <tr>
    <td style="background:#0d0d1a;border:1px solid #2d1b69;border-top:none;padding:24px 40px;">
        <div style="font-size:10px;letter-spacing:2px;text-transform:uppercase;color:#6b7280;margin-bottom:10px;">Summary</div>
        <div style="font-size:13px;color:#9ca3af;line-height:1.8;">{summary}</div>
    </td>
  </tr>
  <tr>
    <td style="background:#030308;border:1px solid #1a1a2e;border-top:none;border-radius:0 0 16px 16px;padding:24px 40px;text-align:center;">
        <div style="font-size:11px;color:#374151;letter-spacing:1px;">
            Powered by <span style="color:#a78bfa;">LangGraph</span> · 
            <span style="color:#a78bfa;">Groq</span> · 
            <span style="color:#a78bfa;">Tavily</span>
        </div>
        <div style="font-size:10px;color:#1f2937;margin-top:8px;">© 2026 Farzi Romano · Unsubscribe anytime</div>
    </td>
  </tr>
</table>
</td></tr>
</table>
</body>
</html>
"""
    else:
        html = f"<html><body><pre>{analysis}</pre></body></html>"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"⚽ {team} Transfer Briefing — {date_str}"
    msg["From"] = f"Farzi Romano <jatinprasad7781@gmail.com>"
    msg["To"] = to_email
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP("smtp-relay.brevo.com", 587) as server:
        server.starttls()
        server.login(login, password)
        server.sendmail(login, to_email, msg.as_string())

    print(f"Email sent to {to_email}!")