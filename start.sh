if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/GamerBhai02/AllMoviesLinkBot.git /AllMoviesLinkBot
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /AllMoviesLinkBot
fi
cd /AllMoviesLinkBot
pip3 install -U -r requirements.txt
echo "Starting AllMoviesLinkBot...."
python3 bot.py
