# Uno

### Summary
This is a little personal project that emulates the very popular card game, UNO. This version can be played between two people and stays true to many of the classic rules of UNO. However, due to the nature of the logic for this game, users are able to stack cards or draw as many cards as they would like. The goal of this is to create more of an open and flexible computer environment for people to pay Uno with, somewhat more closely mimicking the experience in real life compared to other online Uno games. 

### How to Setup
This program can be played online. However, you need to start a server through some website like AWS. Assuming you have an instance in AWS and a key downloaded with the files, you can follow the following steps:
1. In your terminal, navigate to the directory where the key is, and initialize the server with: ssh -i "uno-key.pem" ubuntu@PUBLICIP
2. In a separate terminal, make sure to upload the server file using: scp -i "uno-key.pem" ./server/server.py ubuntu@PUBLICIP:/home/ubuntu/
3. Afterwards navigate to the directory where gui.py is located and run it using: python gui.py
4. Don't forget to stop the server when you're done if you don't want to use more hours than you have to!

### Some More Words
Thanks so much for taking a look at this and reading it! Hopefully this provides a creative base or inspiration for you to make your own Uno implementation (or even another game!). And if you do download this to play, I hope you enjoy!

Have fun!
