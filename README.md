# gsca-pi

GSC User Data API

## Rquestment

    pip install falcon waitress pymongo

## Usage

When you want to launch up server

	python api.py

When you want to get full userdata (upa.ver.2.0.Gsc)

    curl -X GET https://api.限界siege.club/userdata/upa.ver.2.0.Gsc

 When you want to get couple of userdata (upa.ver.2.0.Gsc)

    curl -X GET https://api.限界siege.club/userdata/upa.ver.2.0.Gsc?count=2

When you want to add user id (TennoHanahukku)

    curl -X POST https://api.限界siege.club/userdata/TennoHanahukku

