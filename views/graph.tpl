
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

<div id="content" class="mui-container-fluid" style="margin-left:0px;">
<div id="gDiv" class="tabs">
	<ul class="tab-links">

	</ul>
<div class="tab-content"></div>
</div>
</div>
</html>
<script type="text/javascript">
% for i,gdata in enumerate(gengraph,1):
	% divid = 'div{}'.format(i)
	% divclass, liclass = ('tab active','class="active"') if i==1 else ('tab',' ')
	$(".tab-links").append('<li {{liclass}}><a href="#{{divid}}">Tab#{{i}}</a></li>')
	$("#gDiv .tab-content").append('<div id="{{divid}}" class="{{divclass}}"></div>')
	var data = {{!gdata}}
	Plotly.newPlot('{{divid}}', data.data, data.layout)
% end

</script>

<script>
//http://inspirationalpixels.com/tutorials/creating-tabs-with-html-css-and-jquery
jQuery(document).ready(function() {
jQuery('.tabs .tab-links a').on('click', function(e)  {
var currentAttrValue = jQuery(this).attr('href');
// Show/Hide Tabs
jQuery('.tabs ' + currentAttrValue).show().siblings().hide();
// Change/remove current tab to active
jQuery(this).parent('li').addClass('active').siblings().removeClass('active');
e.preventDefault();
});
});
</script>