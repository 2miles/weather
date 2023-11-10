function temps_list_from_forecast(contextStr) {
  temps = [];
  contextStrDoubleQuotes = contextStr.replaceAll("'", '"');
  forecastObjList = JSON.parse(contextStrDoubleQuotes);
  for (const item of forecastObjList) {
    temps.push(item["temp"]);
  }
  return temps;
}

function buildColorArray() {
  array = [];
  for (let i = 0; i < 25; i += 1) {
    array.push(`rgb(255, ${10 * i}, 25)`);
  }
  array.reverse();
  return array;
}

/* Given a temp and a color array returns an rgb-color-string */
function colorBox(temp) {
  hue = Math.floor(-3 * temp + 300);
  if (temp <= 100 && temp >= 0) {
    hslString = `hsl(${hue}, 100%, 50%)`;
  }
  return hslString;
}

/*

260 - 0
250 - 
---------
230 - 
220 - 
210 - 20
200 - 
190 - 30
180 - 
170 - 40
160 - 
150 - 30
-----------
100 - 
90  - 60
80  -
70  -
60  - 70
50  -
40  -
30  - 80
20  - 85
10  - 90
-------------
340 - 100
330 -
320 -
310 -
300 -

 */

temps = temps_list_from_forecast(forecast);

colorArray = buildColorArray();

let boxes = document.getElementsByClassName("box");

let i = 0;
for (const box of boxes) {
  box.style.backgroundColor = colorBox(temps[i]);
  i += 1;
}
