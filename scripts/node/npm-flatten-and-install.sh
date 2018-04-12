npm ll --parseable | sed 's#\(.*\):\(.*\):\(.*\)#npm install \2#;w ./install-packages.sh' && chmod +x ./install-packages.sh && ./install-packages.sh
