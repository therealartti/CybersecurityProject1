This project was created as an assignment for Helsinki university's Cyber Security Base 2024 course (Project I). It follows Django's 7-part tutorial, while incorporating 5 vulnerabilities:
- Security Misconfiguration
- Security Logging and Monitoring Failures
- Cryptographic Failures
- Broken Access Control
- Injection

Repository Link: https://github.com/therealartti/CybersecurityProject1

### Installation Instructions:

1. Clone the repository:

```git clone https://github.com/therealartti/CybersecurityProject1.git```

2. Navigate to the project directory:

```cd CybersecurityProject1```

3. Install required dependencies (if not already done).

4. Set up the database:

```python manage.py migrate```

5. Start the server:

```python manage.py runserver```

6. Visit http://127.0.0.1:8000/admin/ and login with test:tested123 (username:password) to create a poll.

7. Visit http://127.0.0.1:8000/polls/ to participate in a poll.

### FLAW 1: Insecure Secret Key
Exact Source Link: https://github.com/therealartti/CybersecurityProject1/blob/main/mysite/settings.py#L5

OWASP Risk: Security Misconfiguration

Description of Flaw 1:

The Django application uses an easily guessable secret key ('password'), which Django relies on to create secure signed cookies and other security mechanisms. The password is part of the 10-million-password-list-top-100.txt file that was covered in the Securing Software part IV, which makes it extra susceptible for a brute force attack. This weak secret key lets attackers decipher cookies and potentionally impersonate users, meaning the whole security of the application would be compromised.

How to Fix Flaw 1:

The easiest fix for this flaw is to use a strong, randomly generated secret key. Django even includes a function to get a random secret key throuh its django.core.management.utils package. As mentioned above, replacing the weak key will improve the security posture of the application. The fix is located here: https://github.com/therealartti/CybersecurityProject1/blob/main/mysite/settings.py#L8

Additionally, it is bad practice to store secret keys in the main source code. Instead, storing it in a secure environment variable or a secrets management service is advisable. In the event where the owner's repository gets compromised, the secret would then not be shared.

### FLAW 2: Debug Mode Enabled in Production
Exact Source Link: https://github.com/therealartti/CybersecurityProject1/blob/main/mysite/settings.py#L11

OWASP Risk: Security Logging and Monitoring Failures

Description of Flaw 2:

The Django application has its 'DEBUG' mode enabled, which can expose detailed error information. A potential attacker can then better understand the logic of the backend and easily identify vulnerabilities in the application. When 'DEBUG' mode is active, configuration information are displayed on error pages. That configuration information can include sensitive strings such as secret keys and environment settings.

How to Fix Flaw 2:

Simply disabling the 'DEBUG' parameter prevents the disclosure of sensitive information. By minimizing the error outputs, we can mimimize the risk of exposing the inner workings of the application. The fix is located here: https://github.com/therealartti/CybersecurityProject1/blob/main/mysite/settings.py#L14

It is however recommended to still implement some kind of logging mechanism, which logs errors to a secure server only accessible to authorized people.

### FLAW 3: Insecure Cookie Handling
Exact Source Link: https://github.com/therealartti/CybersecurityProject1/blob/main/mysite/settings.py#L97-L98

OWASP Risk: Cryptographic Failures

Description of Flaw 3:

In our current setup, cookies are configured to be sent over non-HTTPS connections, which gives attackers the opportunity to deploy MITM attacks (man-in-the-middle) against us. An attacker can potentially hijack a user's session and use the given privileges of that user. Cookies often contain or give access to sensitive data.

How to Fix Flaw 3:

To fix this cryptographic failure, we simply change 'CSRF_COOKIE_SECURE' and 'SESSION_COOKIE_SECURE' to True. These settings make sure that the cookies are only sent over HTTPS connections and the data is encrypted during transit, thus enhancing the cookies' security. The fix is located here: https://github.com/therealartti/CybersecurityProject1/blob/main/mysite/settings.py#L101-L102

### FLAW 4: Unauthorized Preview of Upcoming Polls
Exact Source Link: https://github.com/therealartti/CybersecurityProject1/blob/main/polls/views.py#L26

OWASP Risk: Broken Access Control

Description of Flaw 4:

The current implementation lets users see all questions, regardless of their publication date. In case some of the questions are sensitive (such as exam questions), having unauthorized users view polls before they are officially open is not optimal. This could lead to potential advantages or misuse of information before its intended release.

How to Fix Flaw 4: 

We are able to fix this issue by modifying the queryset to filter the questions based on their publication date. This way, only the questiions that are meant to be visible will be accessible to a normal user. The fix is located here: https://github.com/therealartti/CybersecurityProject1/blob/main/polls/views.py#L29

### FLAW 5: SQL Injection
Exact Source Link: https://github.com/therealartti/CybersecurityProject1/blob/main/polls/views.py#L38-L41

OWASP Risk: Injection

Description of Flaw 5:

The vulnerable function uses raw SQL queries directly from user input using string formatting. This flaw makes it vulnerable for SQL injection, which allows a potential attacker to access or change the database information without authorization. Input validation and query parameterization are crucial security measures in modern web development.

How to Fix Flaw 5:

The easiest fix for this flaw is to use Django's ORM methods, thus letting Django handle the parameterization to prevent injection. Parameterization makes it so that the user input is treated strictly as data, not as part of the SQL command. The fix is located here: https://github.com/therealartti/CybersecurityProject1/blob/main/polls/views.py#L44-L55