import sys
import typing

GenericType = typing.TypeVar("GenericType")


class ProgressReport:
    curr_step: typing.Any
    ''' '''

    running: typing.Any
    ''' '''

    start_time: typing.Any
    ''' '''

    steps: typing.Any
    ''' '''

    wm: typing.Any
    ''' '''

    def enter_substeps(self, nbr, msg):
        ''' 

        '''
        ...

    def finalize(self):
        ''' 

        '''
        ...

    def initialize(self, wm):
        ''' 

        '''
        ...

    def leave_substeps(self, msg):
        ''' 

        '''
        ...

    def start(self):
        ''' 

        '''
        ...

    def step(self, msg, nbr):
        ''' 

        '''
        ...

    def update(self, msg):
        ''' 

        '''
        ...


class ProgressReportSubstep:
    final_msg: typing.Any
    ''' '''

    level: typing.Any
    ''' '''

    msg: typing.Any
    ''' '''

    nbr: typing.Any
    ''' '''

    progress: typing.Any
    ''' '''

    def enter_substeps(self, nbr, msg):
        ''' 

        '''
        ...

    def leave_substeps(self, msg):
        ''' 

        '''
        ...

    def step(self, msg, nbr):
        ''' 

        '''
        ...
