def otp_email_template(otp: str) -> str:
    

    return f"""
<!DOCTYPE html>
<html lang="en">

<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NHRC Email Verification</title>
</head>

<body style="
margin:0;
padding:0;
background:#f4f7fb;
font-family:Arial,Helvetica,sans-serif;
">

<table width="100%" cellspacing="0" cellpadding="0" style="background:#f4f7fb;padding:40px 0;">
<tr>
<td align="center">

<table width="650" cellspacing="0" cellpadding="0"
style="
background:#ffffff;
border-radius:10px;
overflow:hidden;
box-shadow:0 4px 15px rgba(0,0,0,0.08);
">

<!-- Header -->
<tr>
<td style="
background:#0056b3;
padding:30px;
text-align:center;
color:white;
">

<h1 style="
margin:0;
font-size:32px;
font-weight:bold;
">
National Human Resource Club
</h1>

<p style="
margin-top:10px;
font-size:16px;
">
Email Verification
</p>

</td>
</tr>

<!-- Body -->
<tr>
<td style="padding:40px;">

<h2 style="
margin-top:0;
color:#333333;
">
Dear User,
</h2>

<p style="
font-size:17px;
line-height:30px;
color:#555555;
">
Thank you for using the
<strong>National Human Resource Club (NHRC)</strong>
portal.
</p>

<p style="
font-size:17px;
line-height:30px;
color:#555555;
">
To verify your email address and continue your registration,
please use the following One-Time Password (OTP).
</p>

<!-- OTP Box -->
<table width="100%" cellspacing="0" cellpadding="0">
<tr>
<td align="center">

<div style="
margin:35px 0;
background:#eef5ff;
border:2px dashed #0056b3;
padding:25px;
border-radius:8px;
display:inline-block;
">

<span style="
font-size:42px;
font-weight:bold;
letter-spacing:10px;
color:#0056b3;
">
{otp}
</span>

</div>

</td>
</tr>
</table>

<!-- Important -->
<h3 style="
color:#d9534f;
margin-bottom:10px;
">
Important
</h3>

<ul style="
color:#555555;
font-size:16px;
line-height:30px;
padding-left:22px;
">

<li>
This OTP is valid for
<strong>10 minutes.</strong>
</li>

<li>
Do not share this OTP with anyone.
NHRC will never ask for your OTP through phone,
email or message.
</li>

<li>
If you did not request this OTP,
please ignore this email.
</li>

</ul>

<hr style="
margin:35px 0;
border:none;
border-top:1px solid #dddddd;
">

<p style="
font-size:16px;
color:#555555;
">
Regards,
</p>

<p style="
font-size:20px;
font-weight:bold;
color:#0056b3;
margin-top:5px;
">
National Human Resource Club
</p>

<p style="
font-size:14px;
color:#888888;
margin-top:25px;
">
This is an automatically generated email.
Please do not reply to this message.
</p>

</td>
</tr>

<!-- Footer -->
<tr>
<td style="
background:#0056b3;
padding:18px;
text-align:center;
color:white;
font-size:13px;
">

© 2026 National Human Resource Club (NHRC)<br>
All Rights Reserved

</td>
</tr>

</table>

</td>
</tr>
</table>

</body>
</html>
"""