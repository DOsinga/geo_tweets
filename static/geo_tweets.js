function draw_shape(processing, shape) {
    if (shape.length <= 1) {
        return;
    }
    processing.beginShape();
    for (var i = 0; i < shape.length; i++) {
        var x1 = shape[i][0];
        var y1 = shape[i][1];
        processing.vertex(x1, y1);
    }
    processing.endShape(processing.CLOSE);
}

function apply_offset(coo, left, right, offset) {
    var x = coo[0] + offset - 720;
    var lst = [];
    if (x < 0) {
        lst = left;
        x += 720;
    } else {
        lst = right;
    }
    lst.push([x, coo[1]])
}


function sketchProc(processing) {

    var offset = 360;

    var autopilot_on = true;

    processing.setup = function() {
        for (var ei = 0; ei < emojis.length; ei++) {
            var emoji = emojis[ei];
            var path = '/static/projects/geo_tweets/by_emoji/' + emoji.img;
            emoji.image = processing.requestImage(path);
        }
        processing.size(720, 300);
        $('#autopilot').click(function() {
            updateFields();
            autopilot_on = !autopilot_on;
            $('#autopilot').text(autopilot_on ? "Auto pilot off" : "Auto pilot on");
        });
    };

    // Override draw function, by default it will be called 60 times per second
    processing.draw = function() {

          var green = 186;
          var blue = 222;
          if (autopilot_on) {
              offset += 0.25;
              if (offset > 720) {
                  offset -= 720;
              }
              var hours = offset / 30 + parseFloat($('#timezone-offset').val()) + 12;
              if (hours > 24) {
                  hours -= 24;
              }
              var hh = Math.floor(hours);
              var mm = Math.floor((hours - hh) * 60);
              if (hh < 10) {
                  hh = '0' + hh;
              }
              if (mm < 10) {
                  mm = '0' + mm;
              }
              $('#current_time').text('' + hh + ':' + mm)
          }
          processing.background(80, green, blue);
          processing.fill(80, blue, green);
          for (var i = 0; i < world_map.length; i++) {
              var left = [];
              var right = [];
              var polygon = world_map[i];
              for (var j = 0; j < polygon.length; j++) {
                  apply_offset(polygon[j], left, right, offset);
              }
              draw_shape(processing, right);
              draw_shape(processing, left);
          }

          var to_plot = [];

          for (var ei = 0; ei < emojis.length; ei++) {
              var emoji = emojis[ei];
              var ioffset_mid = Math.round(offset);
              for (var d_ioffset = -15; d_ioffset < 15; d_ioffset++) {
                  var ioffset = (ioffset_mid + d_ioffset + 360) % 720;
                  var row = emoji.timestamps[ioffset];
                  if (!row) {
                      continue;
                  }
                  for (var i = 0; i < row.length; i++) {
                      var x = row[i][0] / 5 + offset;
                      if (x > 720) {
                          x -= 720;
                      }
                      var y = row[i][1] / 5;
                      to_plot.push([x, y, emoji, d_ioffset]);
                  }
              }
          }

          to_plot.sort();
          for (var tp = 0; tp < to_plot.length; tp++) {
              x = to_plot[tp][0];
              y = to_plot[tp][1];
              emoji = to_plot[tp][2];
              d_ioffset = Math.abs(to_plot[tp][3]);
              var alpha = 255;
              processing.image(emoji.image, x - 16, y - 16, 32, 32);
              if (x < 32) {
                  processing.image(emoji.image, x + 720 - 16, y - 16, 32, 32);
              }
          }
      };

    var mouseLat;
    var mouseLng;

    var ba1 = 1.0; var ba2 = 0.0; var ba3 = 0.0;
    var bb1 = 0.0; var bb2 = 1.0; var bb3 = 0.0;
    var bc1 = 0.0; var bc2 = 0.0; var bc3 = 1.0;


      function sinh(arg) {
          return (Math.exp(arg) - Math.exp(-arg)) / 2;
      }

      processing.keyPressed = function() {
          if(processing.keyCode == processing.UP)
              curRot += 0.04;
          else if(processing.keyCode == processing.DOWN)
              curRot -= 0.04;
          updateFields();
      };

    processing.mousePressed = function() {
        if (autopilot_on) {
            $('#autopilot').click();
        }
        var lat_before = (360 - processing.mouseY) / 180;
        lat_before = Math.atan(sinh(lat_before));
        var lng_before = Math.PI * (processing.mouseX - 360) / 360;
    }
}
