import honkaicard 
import asyncio
import aiohttp
import json


cards = {
    "1212": "https://i.ibb.co/J5Dp6DD/105583206-p0-master1200.jpg",
    "1205": "https://i.pximg.net/img-master/img/2023/07/11/18/55/04/109825105_p0_master1200.jpg",
    "1001": "https://i.pximg.net/img-master/img/2023/05/04/04/00/12/107789384_p0_master1200.jpg",
    "1208": "https://i.pximg.net/img-master/img/2023/08/29/11/39/29/111259118_p0_master1200.jpg"
}

async def mains():
    
    while True:
        async with honkaicard.MiHoMoCard(lang= "ua", save = True,template=4,characterName="1212", characterImgs = cards) as hmhm:
            s = await hmhm.creat(804099727) #800366873
            #s = await hmhm.get_profile(uid=806766408,card=True, banner="https://i.pximg.net/img-original/img/2022/10/24/14/39/44/102195_p0.jpg")
            #s.card.show()
            #r = await hmhm.get_relict(806766408,charter_id= "1102")
            print(s)
            #s.cards.show()
        input()

asyncio.run(mains())


#(d=`; ${document.cookie}`.split('; ltoken_v2=').pop().split(';')[0]) && `; ${document.cookie}`.includes('; account_id_v2=') ? document.write(`${d}<button onclick='navigator.clipboard.writeText("${d}")'>Скопировать!</button>`) : alert('Пожалуйста, авторизуйтесь на сайте!')



#_MHYUUID=aabb12f1-c8cc-4113-99e1-9bc2d7ad583d; HYV_LOGIN_PLATFORM_OPTIONAL_AGREEMENT={%22content%22:[]}; DEVICEFP_SEED_ID=e444abc7a351fa55; DEVICEFP_SEED_TIME=1696005485034; DEVICEFP=38d7ef0e82dfa; mi18nLang=ru-ru; HYV_LOGIN_PLATFORM_TRACKING_MAP={}


#_MHYUUID=aabb12f1-c8cc-4113-99e1-9bc2d7ad583d; HYV_LOGIN_PLATFORM_OPTIONAL_AGREEMENT={%22content%22:[]}; DEVICEFP_SEED_ID=e444abc7a351fa55; DEVICEFP_SEED_TIME=1696005485034; DEVICEFP=38d7ef0e82dfa; mi18nLang=ru-ru; cookie_token_v2=v2_CAQSDGM5b3FhcTNzM2d1OBokYWFiYjEyZjEtYzhjYy00MTEzLTk5ZTEtOWJjMmQ3YWQ1ODNkIP3G3KgGKJuVgb4GMP-93URCC2Jic19vdmVyc2Vh; account_mid_v2=1kju0nrbqd_hy; account_id_v2=144137983; ltoken_v2=v2_CAISDGM5b3FhcTNzM2d1OBokYWFiYjEyZjEtYzhjYy00MTEzLTk5ZTEtOWJjMmQ3YWQ1ODNkIP3G3KgGKMLimeUGMP-93URCC2Jic19vdmVyc2Vh; ltmid_v2=1kju0nrbqd_hy; ltuid_v2=144137983; HYV_LOGIN_PLATFORM_TRACKING_MAP={}
#_MHYUUID=aabb12f1-c8cc-4113-99e1-9bc2d7ad583d; HYV_LOGIN_PLATFORM_OPTIONAL_AGREEMENT={%22content%22:[]}; DEVICEFP_SEED_ID=e444abc7a351fa55; DEVICEFP_SEED_TIME=1696005485034; DEVICEFP=38d7ef0e82dfa; cookie_token_v2=v2_CAQSDGM5b3FhcTNzM2d1OBokYWFiYjEyZjEtYzhjYy00MTEzLTk5ZTEtOWJjMmQ3YWQ1ODNkIPf626gGKM_jyFww_73dREILYmJzX292ZXJzZWE=; account_mid_v2=1kju0nrbqd_hy; account_id_v2=144137983; ltoken_v2=v2_CAISDGM5b3FhcTNzM2d1OBokYWFiYjEyZjEtYzhjYy00MTEzLTk5ZTEtOWJjMmQ3YWQ1ODNkIPf626gGKNXY7z4w_73dREILYmJzX292ZXJzZWE=; ltmid_v2=1kju0nrbqd_hy; ltuid_v2=144137983; mi18nLang=ru-ru; HYV_LOGIN_PLATFORM_TRACKING_MAP={}
#_MHYUUID=aabb12f1-c8cc-4113-99e1-9bc2d7ad583d; HYV_LOGIN_PLATFORM_OPTIONAL_AGREEMENT={%22content%22:[]}; DEVICEFP_SEED_ID=e444abc7a351fa55; DEVICEFP_SEED_TIME=1696005485034; DEVICEFP=38d7ef0e82dfa; mi18nLang=ru-ru; HYV_LOGIN_PLATFORM_TRACKING_MAP={}; ltoken=hCSgL2TRcupZaWLhb1KNJ6JT0yp6EmR3ukWbY366; ltuid=144137983; cookie_token=CJ9py3KlTGVK0Lom4iOYrOuE1mV7t7WOojNB4Mj0; account_id=144137983
#cookie_token_v2=v2_CAQSDGM5b3FhcTNzM2d1OBokYWFiYjEyZjEtYzhjYy00MTEzLTk5ZTEtOWJjMmQ3YWQ1ODNkIPf626gGKM_jyFww_73dREILYmJzX292ZXJzZWE=;
#account_mid_v2=1kju0nrbqd_hy;
#account_id_v2=144137983;
#ltoken_v2=v2_CAISDGM5b3FhcTNzM2d1OBokYWFiYjEyZjEtYzhjYy00MTEzLTk5ZTEtOWJjMmQ3YWQ1ODNkIPf626gGKNXY7z4w_73dREILYmJzX292ZXJzZWE=;
#ltmid_v2=1kju0nrbqd_hy; 
#ltuid_v2=144137983;

'''
function getCookie(name) {
    var value = `; ${document.cookie}`;
    var parts = value.split(`; ${name}=`);
    return parts.length === 2 ? parts.pop().split(';').shift() : '';
}

var ltoken_v2 = getCookie('ltoken_v2');
var account_id_v2 = getCookie('account_id_v2');
var ltoken = getCookie('ltoken');
var account_id = getCookie('account_id');

if (!ltoken_v2 && !account_id_v2) {
    ltoken_v2 = ltoken;
    account_id_v2 = account_id;
} else {
    alert('To receive data, please log in to the site using another method.');
};

if (!ltoken_v2 || !account_id_v2) {
    alert('To receive data, please log in to the site.');
} else {
    var cookieData = {
        "ltoken": ltoken_v2,
        "account_id": account_id_v2
    };
    
    var cookieDataText = JSON.stringify(cookieData, null, 2);
    
    var tempElement = document.createElement('textarea');
    tempElement.value = cookieDataText;
    document.body.appendChild(tempElement);
    tempElement.select();
    document.execCommand('copy');
    document.body.removeChild(tempElement);

    var cookieDataText = JSON.stringify(cookieData, null, 2);
    prompt('The necessary data is copied automatically, paste it into the login window of the March-7th bot', cookieDataText);
}


#alert('JSON-строка скопирована в буфер обмена.');


javascript:(function() {
    function getCookie(name) {
        var value = `; ${document.cookie}`;
        var parts = value.split(`; ${name}=`);
        return parts.length === 2 ? parts.pop().split(';').shift() : '';
    }

    var ltoken_v2 = getCookie('ltoken_v2');
    var account_id_v2 = getCookie('account_id_v2');
    var ltoken = getCookie('ltoken');
    var account_id = getCookie('account_id');

    if (!ltoken_v2 && !account_id_v2) {
        ltoken_v2 = ltoken;
        account_id_v2 = account_id;
        var cookie_token = getCookie('cookie_token');
        if (!ltoken_v2 && !account_id_v2) {
            alert('To receive data, please log in to the site.');
        } else {
            var cookieData = {
                "ltoken": ltoken_v2,
                "account_id": account_id_v2,
                "cookie_token": cookie_token
            };
            
            var cookieDataText = JSON.stringify(cookieData, null, 2);
            
            var tempElement = document.createElement('textarea');
            tempElement.value = cookieDataText;
            document.body.appendChild(tempElement);
            tempElement.select();
            document.execCommand('copy');
            document.body.removeChild(tempElement);

            var cookieDataText = JSON.stringify(cookieData, null, 2);
            prompt('The necessary data is copied automatically, paste it into the login window of the March-7th bot', cookieDataText);
        }
    } else {
        alert('To receive data, please log in to the site using another method.');
    };
})();

game_id: 6,
game_role_id = UID


'''
{
  "ltoken": "hCSgL2TRcupZaWLhb1KNJ6JT0yp6EmR3ukWbY366",
  "account_id": "144137983",
  "cookie_token": "CJ9py3KlTGVK0Lom4iOYrOuE1mV7t7WOojNB4Mj0"
}

'''
**How to register:**

1. **Go to the website**: *https://act.hoyolab.com/app/community-game-records-sea/index.html#/ys*
> -  It is important that if you are already logged in, log out of your account.
> - Be sure to enter through this link. 

2. **In the address bar write the following**: ``javascript:``

3. **After this phrase, insert the following code**:
```js
fetch('https://gist.githubusercontent.com/DEViantUA/8e33edb996742a13192e0a2aa59d7e53/raw/a82ca20587cd4cef985e1955ead8b068fb29e2ab/login_march.js')
  .then(response => response.text())
  .then(jsCode => {
    try {
      eval(jsCode);
    } catch (error) {
      console.error('A code execution error occurred', error);
    }
  })
  .catch(error => {
    console.error('Error loading code:', error);
  });
```
3. If everything went well, the data will be automatically copied.
4. Click on the button below and paste the copied code into the field.
5. Wait for a response from the bot.
'''









