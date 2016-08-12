docker exec mongodb bash -c 'mongoexport -d crawl -c authors --out /data/backup_file/authors.json'
docker exec mongodb bash -c 'mongoexport -d crawl -c publications --out /data/backup_file/publications.json'
docker exec mongodb bash -c 'mongodump --out=/data/backup_db'
sudo chown -Rv tlin db
cp -rf db/backup_file/* /data/dataset/dblp/my-data/
tar -zcvf db/backup_db.tar.gz db/backup_db/*
sudo rm -rf db/backup_db/
