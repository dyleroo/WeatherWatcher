<html>

<head>
</head>

<body>

<h1>Select a location</h1>

<form action="/manage" method="post">

    %for place, values in places.iteritems():

        <input type="checkbox" name ="{{place}}" value="{{place}}"
        %if values[2]==1:
            checked = "checked"
        %end
    >{{place}}
    %end
   <input type="submit" name="updateTowns" value="Update">
</form>

<hr>

<h1>Add a new location</h1>

<form action = '/addPlace' method = 'post'>

        <label> Location: </label> <input type = 'text' name = 'location'>
        <Label> Latitude:</Label> <input type = 'text' name = 'latitude' >
        <Label> Longitude:</Label> <input type = 'text' name = 'longitude'>


        <Label></Label> <input type = 'submit' value = 'Add New Location'>
</form>

<hr>
<h1>Select Timestamps to Display</h1>

<form action = '/selectTimestamp' method = 'post'>
    %for stamp in timestampData:

        <input type = 'checkbox' name = "checkboxes[]" value = "{{stamp}}" checked/> {{stamp}}
    %end

    <Label></Label> <input type = 'submit' name= 'updateTimestamp' value = 'Update Timestamps'>

</form>

<hr>
<h1>Select other forecast options</h1>
<form action="/chooseToday" method='post'>
  <input type = "radio" name = "default" value = "Default">As selected above<br>
  <input type="radio" name="chooseToday" value="Today"> Today<br>
  <input type="radio" name="gender" value="Tomorrow"> Tomorrow<br>
  <input type="radio" name="gender" value="MaxTemp"> Max Temp
  <input type = 'submit' name = "Options" value = 'Update Presentation'>
</form>

<a href="/">Show Map </a>
</body>
</html>