import GLib from 'gi://GLib';

import { LidInhibitor } from '../caffeine@patapon.info/lidInhibitor.js';

const inhibitor = new LidInhibitor();
const loop = new GLib.MainLoop(null, false);

inhibitor.setActive(true);
GLib.timeout_add(GLib.PRIORITY_DEFAULT, 3000, () => {
    inhibitor.destroy();
    loop.quit();
    return GLib.SOURCE_REMOVE;
});

loop.run();
