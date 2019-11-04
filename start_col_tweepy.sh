
#!/bin/sh

cd /app/scripts/

source /app/scripts/venv/bin/activate


echo "Derrubando cargas ativas ..."

ps -ef | grep col_twitter_by_name.py | grep -v grep | awk {'print $2}' | xargs -i kill -9 {}

sleep 5

ps -ef | grep col_twitter_by_name.py | grep -v grep | awk {'print $2}' | xargs -i kill -9 {}

sleep 3
echo "chamando coleta do TOP Trends"
python col_top_trends.py 1

echo "gerando a lista dos  50 ultimos top trends"

for lista in `python col_top_trends.py 2`
do
  sleep 3
  echo $lista
  nohup /app/scripts/venv/bin/python /app/scripts/col_twitter_by_name.py "${lista}" &
done






