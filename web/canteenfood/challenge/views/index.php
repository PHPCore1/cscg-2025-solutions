<html>
<head>
  <meta name='author' content='poory'>
  <meta name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=no'>
  <title>Canteen Plan</title>
  <link rel='stylesheet' href='//maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css' integrity='sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm' crossorigin='anonymous'>
  <link rel='stylesheet' href='//cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.2/css/all.min.css' integrity='sha512-HK5fgLBL+xu6dm/Ii3z4xhlSUyZgTT9tuc/hSrtw6uzJOvgRr2a9jyxxT1ely+B+xFAmJKVSTbpM/CuL7qxO8w==' crossorigin='anonymous' />
  <link rel='stylesheet' href='/static/css/main.css' />
  <link rel='preconnect' href='//fonts.gstatic.com'>
  <link link='preload' href='//fonts.googleapis.com/css2?family=Press+Start+2P&display=swap' rel='stylesheet'>
</head>
<body>
  
<a class='fas fa-heart pulse' href="/admin">admin</a>
<div id='main' class='container'>
  <h1 id='title'>
    <i class='fas fa-heart pulse'></i> <b>Canteen Plan</b> <i class='fas fa-heart pulse'></i>
  </h1>
  <br>
  <div id='img-div'>
    <img id='image' src='/assets/food.gif' alt='yuuuuuuummy'> <!-- Not modified and taken from https://commons.wikimedia.org/wiki/File:Foods_-_Idil_Keysan_-_Wikimedia_Giphy_stickers_2019.gif . Thanks -->
    <br>
  </div>
  <div id='searchfield'>
  <form action="/" method="get">
  <input type="search" id="site-search" placeholder="300" name="price" />
  <button>Cheap Price Search</button>
  </form>
  </div>
  <br>
  <h2>Today we will satisfy you with:</h2> 
  <br>
  <span id='food'> <?= $food ?></span>
</div>
</body>
</html>