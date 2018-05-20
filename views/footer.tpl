	<footer>
	  <div class="mui-container mui--text-center">
		<ul id="pagination" style="text-align:right;">
		% if pagination is not None:
			% for page in pagination:
				<li>{{!page}}</li>
			% end
		% end
		</ul>
	  </div>
	</footer>

  </body>
</html>
