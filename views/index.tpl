% include('header.tpl', tags=tags)

<div id="content" class="mui-container-fluid">

	<div class="mui-row">
		<div class="mui-col-sm-10 mui-col-sm-offset-1">

			<div class="mui--text-dark-secondary mui--text-body2">
				<h1>
					DAILY PYTHON TIPS ({{ len(tips) }})
					% if search_tag:
						<small>&nbsp;(<a href="/">show all</a>)</small>
					% end
				</h1>
			</div>
			<button class="mui-btn mui-btn--primary" onclick="activateModal()">bar chart</button>

			<div class="mui-divider"></div>
			% for tip in tips:
				<div class='tip'>
					<pre>{{ !tip.text }}</pre>
					<div class="mui--text-dark-secondary"><strong>{{ tip.likes }}</strong> Likes / <strong>{{ tip.retweets }}</strong> RTs / {{ tip.created }} / <a href="https://twitter.com/{{screen}}/status/{{ tip.tweetid }}" target="_blank">Share</a></div>
					% like_subclass = "uliked" if int(tip.tweetid) in likes else "nolike"
					<div class="action_div"><span class="action_like {{like_subclass}}" id="like_{{ tip.tweetid }}"><i class="fa fa-heart" aria-hidden="true"></i></span><span class="action_mssg"><i class="fa fa-envelope" aria-hidden="true"></i></span><span class="action_hide">hide</div>

				</div>
			% end

		</div>
	</div>
</div>

% include('footer.tpl')

<script type="text/javascript">

$(".action_like").click(function(){
	
	elem = this;
	subclass = $(elem).attr('class').split(/\s+/)[1].trim();
	tw_id = this.id;
	tw_id = tw_id.split(/[_]+/).pop().trim();
	mparam = {id:tw_id};

	$.ajax({
		url:'/like_a_post?action='+subclass,
		data: mparam,
		type:'post',
		dataType:'json',
		crossDomain:true,
		success:function(json){
			console.log(json);
			if(json["favorited"]){
				$(elem).removeClass(subclass).addClass('uliked') ;
			}
			else{
				$(elem).removeClass(subclass).addClass('nolike');
			}
		    
		},
		error:function( jqXHR, textStatus ) {
		    alert( "Triggered fail callback: " + textStatus );
		}
	});
});

  function activateModal() {
    // initialize modal element
	var $modalEl = $('<div>');
    // set style
    $modalEl.css({
      width: 400,
      height: 200,
      margin: '100px auto',
      backgroundColor: '#fff',

    });

    // add content
    var $formEl = '<form style="padding:15px;">';
    $formEl += '<p><label for="start_limit">start/range1:  </label><input type="text" id="start_limit" value="0"></p>';
    $formEl += '<p><label for="end_limit">end/range2:  </label><input type="text" id="end_limit" value="0"></p>';
    $formEl += '<p><label for="cont">contineous:  </label><input type="checkbox" name="contineous" id="cont"></p>';
    $formEl += '<p><span id="show_graph" class="mui-btn mui-btn--primary mui-btn--small" onclick="showGraph()">show_graph</span></p>';
    $formEl +='</form>';
    $modalEl.append($formEl);

    // show modal
    mui.overlay('on', $modalEl.get(0));
  }


function showGraph(){

	startlimit =  $("#start_limit").val();
	endlimit = $("#end_limit").val();
	contineous = $('input[name="contineous"]').is(':checked') ? 1:0 ;

	var link = document.createElement('a');
	$(link).attr('target', '_blank');
	url='/show_graph?start='+startlimit+'&end='+endlimit+'&contineous='+contineous
	link.href = url;
	document.body.appendChild(link);
	link.click();
	mui.overlay('off', $modalEl) 
}
</script>