import sciluigi as sl
import logging
import os

log = logging.getLogger('luigi-interface')

class MyFooWriter(sl.Task):
    # We have no inputs here
    basepath = sl.Parameter()
    task_namespace = 'prep'
    # Define outputs:
    def out_foo(self):
        return sl.TargetInfo(self, os.path.join(self.basepath, 'foo.txt'))

    def run(self):
        log.info("Running MyFooWriter")
        with self.out_foo().open('w') as foofile:
            foofile.write('foo\n')

class MyFooReplacer(sl.Task):
    basepath = sl.Parameter()
    task_namespace = 'prep'
    replacement = sl.Parameter() # Here, we take as a parameter
                                  # what to replace foo with.
    # Here we have one input, a "foo file":
    in_foo = None
    # ... and an output, a "bar file":

    def out_replaced(self):
        # As the path to the returned target(info), we
        # use the path of the foo file:
        return sl.TargetInfo(self, self.in_foo().path + '.bar.txt')

    def run(self):
        log.info("Running MyFooReplacer")
        with self.in_foo().open() as in_f:
            with self.out_replaced().open('w') as out_f:
                # Here we see that we use the parameter self.replacement:
                out_f.write(in_f.read().replace('foo', self.replacement))