

checkname = 'esx_vsphere_sensors'


info = [
    ['VMware Rollup Health State', '', '0', 'system', '0', '', 'red', 'Red',
     'Sensor is operating under critical conditions'],
    ['Power Domain 1 Power Unit 0 - Redundancy lost', '', '0', 'power', '0', '',
     'yellow', 'Yellow', 'Sensor is operating under conditions that are non-critical'],
    ['Power Supply 2 Power Supply 2 0: Power Supply AC lost - Assert', '', '0', 'power',
     '0', '', 'red', 'Red', 'Sensor is operating under critical conditions'],
    ['Dummy sensor', '', '', '', '', '', 'green', 'all is good', 'the sun is shining']
]


discovery = {'': [(None, [])]}


checks = {
    '': [(None, 'default', [
            (2, 'VMware Rollup Health State: Red (Sensor is operating under critical '
             'conditions)', []),
            (1, 'Power Domain 1 Power Unit 0 - Redundancy lost: Yellow '
             '(Sensor is operating under conditions that are non-critical)', []),
            (2, 'Power Supply 2 Power Supply 2 0: Power Supply AC lost - Assert: Red '
             '(Sensor is operating under critical conditions)', []),
            (0, ('\nAt least one sensor reported. Sensors readings are:\n'
                 'VMware Rollup Health State: Red (Sensor is operating under critical conditions)\n'
                 'Power Domain 1 Power Unit 0 - Redundancy lost: Yellow (Sensor is operating under conditions that are non-critical)\n'
                 'Power Supply 2 Power Supply 2 0: Power Supply AC lost - Assert: Red (Sensor is operating under critical conditions)\n'
                 'Dummy sensor: all is good (the sun is shining)'), [])]
         ),
    ],
}