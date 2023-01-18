import googleapiclient.discovery


driveService = googleapiclient.discovery.build('drive', 'v3', http = httpAuth) # Выбираем работу с Google Drive и 3 версию API
access = driveService.permissions().create(
    fileId = spreadsheetId,
    body = {'type': 'user', 'role': 'writer', 'emailAddress': 'baranchukoff@gmail.com'},  # Открываем доступ на редактирование
    fields = 'id'
).execute()