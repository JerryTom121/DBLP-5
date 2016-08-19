docker exec mongodb bash -c 'tar xv -C / -f /data/backup_db.tar.gz'
docker exec mongodb bash -c 'mongorestore --db crawl /db/backup_db/crawl'
sudo rm -rf db/tmp/
