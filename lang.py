from config import RUS_or_ENG
s=RUS_or_ENG

check_server="Check Servers" if s else "Проверить сервера"
check_user="Get user" if s else "Получить пользователя"
actions="Choose action" if s else "Выберите действие"
server_running="Server is running" if s else "Сервер запущен"
server_stopped="Server is stopped" if s else "Сервер не запущен"
usage="Usage" if s else "Потребление"
startserver="Start" if s else "Запустить"
restartserver="Restart" if s else "Перезапустить"
killserver="Kill" if s else "Убить сервер"
stopserver="Stop" if s else "Остановить"
l_username="Username" if s else "Пользователь"
l_name="Name" if s else "Имя"

l_started="Server starting..." if s else "Сервер запускается..."
l_stopped="Server stopped..." if s else "Сервер остановлен..."
l_restarted="Server restarting..." if s else "Сервер перезапускается..."

l_execute="Exucute command in console" if s else "Выполнить команду в консоль"
l_executed="Command executed" if s else "Команда выполнена"
l_command="Command" if s else "Команда"
l_typecommand="Type command" if s else "Введите команду"