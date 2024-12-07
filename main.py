import shutil
import os

def create_html_file(folder_name, page_title, buttons, logo, about):
    html_content = f'''<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title}</title>
    <link rel="shortcut icon" type="image/icon" href="{os.path.basename(logo)}">
    <link rel="stylesheet" href="styles.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="scripts.js"></script>
    
</head>
<body dir="rtl">
    <div class="container">
        <button id="toggle-theme" class="theme-toggle-btn">
            <i class="fas fa-sun" data-theme="light"></i>
            <i class="fas fa-moon" data-theme="dark"></i>
        </button>
        <header>
            <img src="{os.path.basename(logo)}" alt="صورة شخصية" class="profile-img">
            <h1>{page_title}</h1>
            <p class="bio">{about}</p>
        </header>
        <main>
            <div class="links">
    '''

    # إضافة الأزرار
    for title, link in buttons:
        html_content += f'''
                <div class="link-container">
                    <a href="{link}" target="_blank" class="link">{title}</a>
                    <button class="copy-btn" data-url="{link}"><i class="fas fa-copy"></i></button>
                </div>
        '''

    # استكمال باقي محتوى HTML
    html_content += '''
            </div>
            <button id="show-message-form-btn" class="message-form-btn">أرسل رسالة | Send a Message</button>
        </main>
        <footer>
            <p>&copy; جميع الحقوق محفوظة 2024</p>
        </footer>
    </div>
    <div id="copy-alert" class="alert" style="display: none;">تم نسخ الرابط إلى الحافظة!</div>
    <div id="message-form" class="message-form" style="display: none;">
        <form method="post">
            <textarea id="message-textarea" placeholder="اكتب رسالتك هنا..."></textarea>
            <button id="send-message-btn" type="submit">إرسال</button>
            <button id="close-message-form" type="button">إغلاق</button>
        </form>
    </div>
    <div id="Box">
        <div id="alertBox" class="d-none"></div>
    </div>
        <script>
        $(document).ready(function() {
            // Handle show message form button
            $("#show-message-form-btn").click(function() {
                $("#message-form").show();
            });

            // Handle close message form button
            $("#close-message-form").click(function() {
                $("#message-form").hide();
            });

            // Handle form submission
            $("#message-form form").submit(function(event) {
                event.preventDefault();

                var form = $(this);
                var submitButton = form.find("button[type='submit']");
                var messageTextarea = form.find("textarea");
                var alertBox = $("#alertBox");

                if (submitButton.prop('disabled')) {
                    return; // منع النقر إذا كان الزر معطلاً
                }

                var message = messageTextarea.val().trim();
                if (message) {
                    var originalText = submitButton.text(); // حفظ النص الأصلي للزر
                    submitButton.html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> جاري إرسال الرسالة'); // استبدال النص بعلامة التحميل
                    submitButton.prop('disabled', true); // تعطيل الزر لمنع النقر المتكرر

                    $.ajax({
                        url: 'sendmg.php', // Replace with the correct path
                        type: 'POST',
                        data: { message: message },
                        dataType: 'json',
                        success: function(response) {
                            var alertClass = response.status === 'success' ? 'alert-success' : 'alert-danger';
                            alertBox
                                .removeClass('d-none alert-success alert-danger') // إزالة جميع فئات التنبيه السابقة
                                .addClass(alertClass) // إضافة الفئة المناسبة بناءً على حالة الرد
                                .html(response.message) // عرض الرسالة
                                .show();

                            setTimeout(function() {
                                alertBox.fadeOut(500, function() {
                                    $(this).removeClass(alertClass).addClass('d-none').html(''); // إعادة ضبط التنبيه
                                });
                            }, 2000);

                            messageTextarea.val(''); // تفريغ النص
                            $("#message-form").hide(); // إخفاء النموذج بعد الإرسال
                        },
                        error: function(xhr, status, error) {
                            alertBox
                                .removeClass('d-none alert-success')
                                .addClass('alert-danger')
                                .html('فشل في إرسال الرسالة.')
                                .show();

                            setTimeout(function() {
                                alertBox.fadeOut(500, function() {
                                    $(this).removeClass('alert-danger').addClass('d-none').html(''); // إعادة ضبط التنبيه
                                });
                            }, 2000);
                        },
                        complete: function() {
                            submitButton.html(originalText); // إعادة النص الأصلي بعد انتهاء العملية
                            submitButton.prop('disabled', false); // تمكين الزر مرة أخرى
                        }
                    });
                } else {
                    alertBox
                        .removeClass('d-none alert-success alert-danger')
                        .addClass('alert-warning')
                        .html('من فضلك أدخل رسالة.')
                        .show();

                    setTimeout(function() {
                        alertBox.fadeOut(500, function() {
                            $(this).removeClass('alert-warning').addClass('d-none').html(''); // إعادة ضبط التنبيه
                        });
                    }, 2000);
                }
            });
        });
    </script>
</body>
</html>
    '''
   
    

    # حفظ ملف HTML
    file_path = os.path.join(folder_name, "index.html")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(html_content)
    print(f"try move")
    shutil.move(logo,folder_name)
    print(f"done")
    print(f"Html File saved successfully: {file_path}")




def create_css_file(folder_name, darkcolor, lightcolor,ContainerBgLight,ContainerBgDark,ButtonBgLight,ButtonBgDark):
    css_content = '''
/* Reset some default styles */
body, h1, p, a {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Arial', sans-serif;
    transition: background 0.3s ease, color 0.3s ease;
    background: var(--bg-color);
    color: var(--text-color);
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    margin: 0;
    padding:50px 0px;
}

.container {
    background: var(--container-bg);
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
    max-width: 400px;
    width: 70%;
    padding: 25px;
    text-align: center;
    position: relative;
    overflow: hidden;
    transform: translateY(0);
    transition: transform 0.3s ease-in-out;
}

.container:hover {
    transform: translateY(-10px);
}

header {
    margin-bottom: 25px;
}

.profile-img {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    object-fit: cover;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    transition: transform 0.4s ease, box-shadow 0.4s ease;
}

.profile-img:hover {
    transform: scale(1.1);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
}

h1 {
    font-size: 32px;
    color: var(--header-color);
    margin: 15px 0;
    animation: fadeIn 1s ease-in-out;
}

.bio {
    color: var(--bio-color);
    font-size: 18px;
    margin-bottom: 25px;
    animation: fadeIn 1.5s ease-in-out;
}

.links {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.link-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: relative;
    padding:0px -100px;
}

.link {
    display: flex;
    align-items: center;
    padding: 15px;
    background: var(--link-bg);
    color: var(--link-text);
    border-radius: 12px;
    text-decoration: none;
    font-size: 12px;
    transition: background 0.4s ease, transform 0.4s ease;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
    position: relative;
    width: 100%;
    justify-content: space-between;
}

.link:hover {
    background: var(--link-hover-bg);
    transform: translateY(-5px);
}

.copy-btn {
    background: var(--bg-copy);
    border: none;
    border-radius: 5px;
    color: #fff;
    padding: 5px 10px;
    font-size: 14px;
    cursor: pointer;
    transition: background 0.3s ease;
    position: absolute;
    left: 20px;
}

.copy-btn:hover {
    background: var(--copy-hover-bg);
}

.copy-btn i {
    margin-left: 5px;
}
footer {
    margin-top: 25px;
    color: var(--footer-color);
    font-size: 14px;
}

.theme-toggle-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 10px;
    background: var(--btn-bg);
    color: var(--btn-text);
    border: none;
    border-radius: 50%;
    cursor: pointer;
    transition: background 0.3s ease, transform 0.3s ease;
    position: relative;
    width: 50px;
    height: 50px;
    font-size: 20px;
}

.theme-toggle-btn i {
    position: absolute;
    transition: opacity 0.3s ease;
}

.theme-toggle-btn .fa-sun {
    opacity: 1;
}

.theme-toggle-btn .fa-moon {
    opacity: 0;
}

[data-theme="dark"] .fa-sun {
    opacity: 0;
}

[data-theme="dark"] .fa-moon {
    opacity: 1;
}

.theme-toggle-btn:hover {
    background: var(--btn-hover-bg);
    transform: scale(1.1);
}

.alert {
    direction: rtl;
    background-color: #4caf50; /* اللون الأخضر للإشعار الناجح */
    color: #fff;
    opacity: 1;
    transition: opacity 0.6s;
    position: fixed;
    z-index: 1299;
    bottom: 30px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    justify-content: center;
    padding: 20px 6px;
    border-radius: 5px;
    font-size: 16px;
}

.message-form-btn{
    display: flex;
    align-items: center;
    padding: 15px;
    background: var(--link-bg);
    color: var(--link-text);
    border-radius: 12px;
    text-decoration: none;
    font-size: 18px;
    transition: background 0.4s ease, transform 0.4s ease;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
    position: relative;
    width: 100%;
    margin-top:20px;
    justify-content: space-between;
}
.message-form-btn:hover {
    background: var(--link-hover-bg);
    transform: translateY(-5px);
}
.message-form {
    position: fixed;
    top: 45%;
    left: 50%;
    transform: translateX(-50%);
    background: var(--container-bg);
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    padding: 20px;
    width: 90%;
    max-width: 500px;
    z-index: 999;
    color: var(--text-color);
}

.message-form textarea {
    width: 100%;
    height: 150px;
    padding: 10px;
    border: 1px solid var(--text-color);
    text-align: center;
    border-radius: 5px;
    margin-bottom: 10px;
    box-sizing: border-box;
    background: var(--bg-color);
    color: var(--text-color);
}

.message-form button {
    background: var(--btn-bg);
    border: none;
    border-radius: 5px;
    color: var(--btn-text);
    padding: 10px;
    cursor: pointer;
    transition: background 0.3s ease;
    margin-right: 5px;
}

.message-form button:hover {
    background: var(--btn-hover-bg);
}
#Box {
    display: flex;
    align-items: center;
    justify-content: center;
}
#alertBox {
    display: block; /* يبدأ مخفيًا */
    max-width: 100%;
        position:fixed;
    z-index:999;
    bottom:20px;
    padding: 15px 150px;
    margin-top: 10px;
    font-size: 16px;
    font-weight: 500;
    border-radius: 5px;
    color: #fff;
    text-align: center;

    transition: opacity 0.5s ease, transform 0.5s ease;
}

#alertBox.alert-success {
    background-color: #28a745;
    border: 1px solid #28a745;
}

#alertBox.alert-danger {
    background-color: #dc3545;
    border: 1px solid #dc3545;
}

#alertBox.alert-warning {
    background-color: #ffc107;
    border: 1px solid #ffc107;
}

#alertBox.alert-info {
    background-color: #17a2b8;
    border: 1px solid #17a2b8;
}

#alertBox.show {
    display: block; /* إظهار العنصر */
    opacity: 1;
    transform: translateY(0);
}

#alertBox.fade {
    opacity: 0;
    transform: translateY(-10px);
    display: none; /* إخفاء العنصر بعد اختفاء التأثير */
}

/* Animation keyframes */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Day theme */
/* Day theme */
:root {
    --bg-color: '''+lightcolor+''';
    --text-color: #333;
    --container-bg: '''+ContainerBgLight+''';
    --accent-color: #735e99;
    --header-color: #333;
    --bio-color: #666;
    --link-bg: '''+ButtonBgLight+''';
    --link-text: #fff;
    --link-hover-bg: #99b3ff;
    --footer-color: #666;
    --btn-bg: #19237d;
    --btn-text: #fff;
    --btn-hover-bg: #99b3ff;
    --bg-copy:#007bff;
    --copy-hover-bg: #99b3ff;
}

/* Night theme */
[data-theme="dark"] {
    --bg-color:'''+darkcolor+''';
    --text-color: #e0e0e0;
    --container-bg: '''+ContainerBgDark+''';
    --accent-color: #400080;
    --header-color: #e0e0e0;
    --bio-color: #ccc;
    --link-bg: '''+ButtonBgDark+''';
    --link-text: #fff;
    --link-hover-bg: #400080b9;
    --footer-color: #ccc;
    --btn-bg: #400080;
    --btn-text: #fff;
    --btn-hover-bg: #400080b9;
    --bg-copy:#6000c0;
    --copy-hover-bg: #400080b9;
}
/* Responsive Design */
@media (max-width: 768px) {
    .profile-img {
        width: 110px;
        height: 110px;
    }

    h1 {
        font-size: 28px;
    }

    .bio {
        font-size: 16px;
    }

    .link {
        font-size: 16px;
        padding: 12px;
    }

    .theme-toggle-btn {
        width: 40px;
        height: 40px;
        font-size: 18px;
    }
    #alertBox {
                padding: 15px 100px;
        }
}

@media (max-width: 480px) {
    .profile-img {
        width: 90px;
        height: 90px;
    }

    h1 {
        font-size: 24px;
    }

    .bio {
        font-size: 14px;
    }

    .link {
        font-size: 14px;
        padding: 10px;
    }

    .container {
        padding: 20px;
    }

    .theme-toggle-btn {
        width: 35px;
        height: 35px;
        font-size: 16px;
    }
            #alertBox {
                padding: 10px 30px;
        }
}


'''
    file_path = os.path.join(folder_name, "styles.css")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(css_content)

    print(f"CSS file saved successfully: {file_path}")

def create_js_file(folder_name):
    js_content = '''
document.addEventListener('DOMContentLoaded', function() {
    const toggleButton = document.getElementById('toggle-theme');
    const showMessageFormBtn = document.getElementById('show-message-form-btn');
    const messageForm = document.getElementById('message-form');
    const closeMessageFormBtn = document.getElementById('close-message-form');
    const sendMessageBtn = document.getElementById('send-message-btn');
    const messageTextarea = document.getElementById('message-textarea');
    const alertBox = document.getElementById('copy-alert');
    
    // Check if the user has a preference stored
    const currentTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', currentTheme);

    toggleButton.addEventListener('click', () => {
        const theme = document.documentElement.getAttribute('data-theme');
        const newTheme = theme === 'light' ? 'dark' : 'light';
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    });

    // Add copy functionality only to specific buttons
    const copyButtons = document.querySelectorAll('.copy-btn');

    copyButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault(); // Prevent the button from causing any default action
            const url = button.getAttribute('data-url');
            navigator.clipboard.writeText(url).then(() => {
                alertBox.innerHTML = 'ØªÙ… Ù†Ø³Ø® Ø§Ù„Ø±Ø§Ø¨Ø· Ø¥Ù„Ù‰ Ø§Ù„Ø­Ø§ÙØ¸Ø©!';
                alertBox.style.background = 'green';
                alertBox.style.padding = '16px 50px';
                alertBox.style.display = 'flex';
                setTimeout(() => {
                    alertBox.style.opacity = 0;
                    setTimeout(() => {
                        alertBox.style.display = 'none';
                        alertBox.style.opacity = 1;
                    }, 600);
                }, 2000);
            }).catch(err => {
                console.error('Copy failed: ', err);
            });
        });
    });

});

    '''

    file_path = os.path.join(folder_name, "scripts.js")
    with open(file_path, "w",encoding="utf-8") as file:
        file.write(js_content)

    print(f"Javascript File saved successfully: {file_path}")

def create_php_file(folder_name,name,email):
    php_content='''
<?php
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

require 'PHPMailer-master/src/Exception.php';
require 'PHPMailer-master/src/PHPMailer.php';
require 'PHPMailer-master/src/SMTP.php';

$dbhost = 'pdb1050.awardspace.net';
$dbname = '4438085_devadnan';
$username = '4438085_devadnan';
$password = 'Adnan&&123';

try {
    $conn = new PDO("mysql:host=$dbhost;dbname=$dbname", $username, $password);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch(PDOException $e) {
    error_log("Database connection failed: " . $e->getMessage());
    echo json_encode(['status' => 'error', 'message' => 'فشل الاتصال بالقاعدة']);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['message'])) {
    $name = '''+name+'''
    $email = '''+email+'''
    try {
        $message = htmlspecialchars($_POST['message']);
        if (empty($message)) {
            throw new Exception('رسالة فارغة');
        }

        $stmt = $conn->prepare("INSERT INTO message (message_text) VALUES (:message_text)");
        $stmt->bindParam(':message_text', $message);
        $stmt->execute();

        $mail = new PHPMailer(true);
        $mail->isSMTP();
        $mail->Host = 'mboxhosting.com';
        $mail->SMTPAuth = true;
        $mail->Username = 'admin@devadnan.net';
        $mail->Password = 'Adnan123';
        $mail->SMTPSecure = 'STARTTLS';
        $mail->Port = 587;
        $mail->CharSet = 'UTF-8';
        $mail->setFrom('info@devadnan.net', 'DevAdnan');
        $mail->addAddress($email,$name);
        $mail->Subject = "رسالة جديدة في موقعك";
        $mail->isHTML(true);
        $mail->Body = <<<HTML
            <html>
                <body style="direction: rtl; text-align: center; font-family: Arial, sans-serif; background-color: #fff; padding: 20px;">
                    <div style="max-width: 600px; margin: auto; background-color: #2a2a2a; padding: 20px; border: 1px solid #dddddd; border-radius: 10px;">
                        <img src="https://devadnan.net/assets/images/about/logo.png" alt="Header Image" style="width: 100%; border-radius: 10px 10px 0 0;">
                        <h1 style="color: #fff; text-align: center;">مرحبًا $name !</h1>
                        <p style="font-size: 16px; color: #fff;">تم تسجيل رسالة جديدة في موقعك.</p>
                        <h2 style="color: #fff;">المعلومات</h2>
                        <ul style="list-style: none; padding: 0; color: #fff; text-align: right;">
                            <li>✔ الرسالة: $message</li>
                        </ul>
                        <div style="text-align: center; margin: 20px 0;">
                            <a href="https://devadnan.net" style="background-color: #337ab7; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">زوروا متجرنا</a>
                        </div>
                        <hr style="border: none; border-top: 1px solid #dddddd;">
                        <p style="font-size: 14px; color: #fff;">مع أطيب التحيات،<br>عدنان<br>مالك الموقع DevAdnan.net</p>
                    </div>
                </body>
            </html>
        HTML;

        $mail->send();
        echo json_encode(['status' => 'success', 'message' => 'تم إرسال الرسالة بنجاح']);
    } catch (Exception $e) {
        error_log("Error: " . $e->getMessage());
        echo json_encode(['status' => 'error', 'message' => 'فشل في إرسال الرسالة']);
    }
} else {
    echo json_encode(['status' => 'error', 'message' => 'رسالة غير محددة']);
}
?>

 '''


    file_path = os.path.join(folder_name, "sendmg.php")
    with open(file_path, "w",encoding="utf-8") as file:
        file.write(php_content)

    print(f"php File saved successfully: {file_path}")



folder_name = input("Enter name of folder: ex(Adnan) ")
try:
    os.makedirs(folder_name, exist_ok=True)
    print(f"Folder '{folder_name}' created successfully.")
except Exception as e:
    print(f"Error creating folder: {e}")
page_title = input("Enter the name of the title: ex(Adnan alharbi) ")
logo = input("Enter the path of logo: ex(logo.png) ")
about = input("Enter the text about: ex(softwaer programmer)")

try:
    button_count = int(input("How many buttons do you want? ex(2)"))
    if button_count < 1:
        raise ValueError("Button count must be greater than zero.")
except ValueError as e:
    print(f"Invalid input: {e}")
    button_count = 1

buttons = []

for i in range(button_count):
    title = input(f"Name of Button {i + 1}: ex(SnapChat) ")
    link = input(f"URL of Button {i + 1}: ex(https://www.snapchat.com/add/devadnan?share_id=ManbRTACg54&locale=ar-AE)")
    buttons.append((title, link))
light = input("Enter the color of lightcolor : ex(#fff)")
dark = input("Enter the color of the darkcolor: ex(#000)")
ContainerBgLight = input("Enter the color of the ContainerBgLight: ex(#eee)")
ContainerBgDark = input("Enter the color of the ContainerBgDark: ex(#2a2a2a)")
ButtonBgLight = input("Enter the color of the Bg Color Light: ex(#3248a8)")
ButtonBgDark = input("Enter the color of the Bg Color Dark : ex(#a432a8)")
nameofres = input("Enter the name of Recipient: ex(Adnan) ")
emailofres = input("Enter the email of Recipient: ex(info@devadnan.net) ")
create_html_file(folder_name, page_title, buttons,logo,about)
create_css_file(folder_name, dark, light,ContainerBgLight,ContainerBgDark,ButtonBgLight,ButtonBgDark)
create_js_file(folder_name)
create_php_file(folder_name,nameofres,emailofres)