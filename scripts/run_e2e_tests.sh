# Init database
python manage.py init_test_db

# Launch server in background
python manage.py runserver 0.0.0.0:8000 &
SERVER_PID=$!

# Waiting for server to be ready
sleep 3

# run E2E tests
pytest core/tests/test_end_to_end.py

# stop serveur
kill $SERVER_PID
