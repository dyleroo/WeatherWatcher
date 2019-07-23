<html>
<head>
    <title>OpenWeatherMap Forecasts</title>
</head>
<body style="padding: 0px">
    <img src='images/ireland.png'>

    <div style="position: absolute; top:30; left:0; width: 200;
                background-color: rgb(255, 255, 150)">
      <h3 style="font-family: calibra, arial; position:relative;
                left:30;">{{ timestampData }}</h3>
</div>

%for symbol in mapData:
    %if symbol[4] in chosenLocations:
        <div style="position:absolute; left:{{ symbol[0] }};
                    top:{{ symbol[1] }}">
            <svg height='26' width='26'>
                <g>
                    <circle cx='13' cy='13' r='13'
                        stroke-width='0' fill='red' />
                    <text x='50%' y='50%' stroke='#fff' fill='#fff'
                            stroke-width='1px' text-anchor='middle'
                            dy='0.3em'>
                            {{ symbol[3] }}
                    </text>
                </g>
            </svg>
            <span style='position: relative; top:-10;
                         background-color: #ff0; opacity: 0.6;
                         padding: 4px; font-weight: bold'>
                    {{ symbol[4] }}</span> <br>
            <img src='{{ symbol[2] }}'
                style='position:relative; top:-70; left:-10'>
        </div>
    %end
%end

    <div style="width:540; text-align: center">
        <a href = "/{{ prev }}">
            <img src='images/previous.png'
                style='padding-right:40; width:50'></a>
        <a href = "/{{ next }}">
            <img src='images/next.png'
                 style='padding-left: 40; width:50'></a>
    </div>
</body>
    <a href='/manage'>Click here to manage</a>
</html>