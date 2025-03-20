if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/vivekdevx/AutoFilterX.git /VeerHanumanBot
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /VeerHanumanBot
fi
cd /VeerHanumanBot
pip3 install -U -r requirements.txt
echo "Starting VeerHanumanBot...."
python3 bot.py
