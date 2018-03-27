
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="//cdn.muicss.com/mui-0.9.28/css/mui.min.css" rel="stylesheet" type="text/css" />
    <link href="static/css/style.css" rel="stylesheet" type="text/css" />
    <link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet" type="text/css">
    <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <script src="//cdn.muicss.com/mui-0.9.28/js/mui.min.js"></script>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <title>Daily Python Tip</title>
  </head>
  <body>

<div id="content" class="mui-container-fluid">
<div id="gDiv"></div>
</div>
</html>
<script type="text/javascript">
var gdata = {{!graphData}}
Plotly.newPlot('gDiv', gdata.data, gdata.layout);

</script>