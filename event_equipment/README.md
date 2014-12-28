[ NAME ]
event_equipment


[ SUMMARY ]
Events - equipment


[ AUTHOR ]
Rui Pedrosa Franco


[ VERSION ]
8.0.1.0


[ WEBSITE ]
http://pt.linkedin.com/in/ruipedrosafranco


[ CATEGORY ]
Extra Tools


[ LICENSE ]
AGPL-3


[ DESCRIPTION ]

                        - Allows to define lists of equipment associated to an event
                        - Partners may define what kind of equipment they possess (from the ones associated to any event they have registered in)
                        - Equipment can be associated to the attendants or to the event itself
                        - Partner field is shown in the event's registration lines
                        - Equipment lists can be associated to event types
                        - Event type becomes mandatory
                        - More fields are shown in the event type tree view
                        
                        NOTE:
                        - (event.event) equipment_host_text and equipment_participants_text hold the equipment list as text
                        


[ MENUS ]



[ VIEWS ]
* INHERIT event_equipment_view_event_form (form)
* INHERIT event_equipment_view_event_type_form (form)
* INHERIT event_equipment_view_event_type_tree (tree)
* INHERIT event_equipment_view_partner_form (form)
report_equipment_host (qweb)
report_equipment_host_document (qweb)


[ REPORTS ]
Equipment (host)