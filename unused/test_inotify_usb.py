import inotify.adapters

def _main():
    i = inotify.adapters.Inotify()

    i.add_watch('/dev/sda1')
    i.add_watch('/dev/sda2')
    i.add_watch('/dev/sda3')
    i.add_watch('/dev/sda4')
    i.add_watch('/dev/sda5')
    i.add_watch('/dev/sda6')

    with open('/tmp/test_file', 'w'):
        pass

    for event in i.event_gen(yield_nones=False):
        (_, type_names, path, filename) = event

        print("PATH=[{}] FILENAME=[{}] EVENT_TYPES={}".format(
              path, filename, type_names))

if __name__ == '__main__':
    _main()
