For lunch application docker and docker compose should be installed
I added default db with default data but if you want you can delete current one and create new

if you want just run app without creating db just run frm cola folder
    docker-compose up -d --build

in other case to init default db :

1. build application from terminal:
    docker-compose up -d --build

2. copy container id:
    docker ps

3. run command to get access to bash
    docker exec -it {cola_app_container_id} bash

4. in bash run
    python

5. from python console run default migration to create db and init default data
    from db.migration import init_db
    init_db()

can test via postman

    urls:
        - http://172.18.0.3:5000/api/auth          - for auth (Base auth) via psw and username (POST)
            pepsiUser
            pepsiPsw

            cocaUser
            cocaPsw

        You should add Token to x-access-token Header to get access to other endpoint

        - localhost:5000/api/shifts/all             - get all shifts (GET)

        - http://172.18.0.3:5000/api/shifts/add     - add new shift(POST)
            data example to send
            {
                "room_id" : 1, int
                "hours_from" : "16", str
                "minutes_from" : "15",str
                "hours_to" : "17", str
                "minutes_to" : "15" str
            }

        -  http://172.18.0.3:5000/api/shifts/delete/{shift_id) - delete shift by id (DELETE)
            example: http://172.18.0.3:5000/api/shifts/delete/3

