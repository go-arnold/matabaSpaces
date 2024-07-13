$(document).ready(function() {



    $('#calendar').fullCalendar({

      header: {

        left: 'prev,next today',

        center: 'title',

        right: 'month,agendaWeek,agendaDay'

      },

      defaultDate: '2024-09-01',

      navLinks: true, // can click day/week names to navigate views

      selectable: true,

      selectHelper: true,

      select: function(start, end) {

        var title = prompt('Event Title:');

        var eventData;

        if (title) {

          eventData = {

            title: title,

            start: start,

            end: end

          };

          $('#calendar').fullCalendar('renderEvent', eventData, true); // stick? = true

        }

        $('#calendar').fullCalendar('unselect');

      },

      editable: true,

      eventLimit: true, // allow "more" link when too many events

      events: [

        


        {

          title: 'Scheduled Graduation',

          start: '2024-12-22',

          

        },
      

        {

          title: 'Start Date Defense',

          start: '2024-08-15T17:30:00'

        },

        {

          title: 'EndDate of defense',

          start: '2024-09-22T20:00:00'

        },

        {

          title: 'Arnold 22nd Birthday',

          start: '2024-10-02T07:00:00'

        },

        {

          title: 'Verify my ULK MIS ',

          url: 'https://mis.ulk.ac.rw/',

          start: '2024-10-12'

        }

      ]

    });



  });