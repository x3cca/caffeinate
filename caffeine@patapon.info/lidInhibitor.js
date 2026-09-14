/**
 * Caffeinate lid-switch integration.
 *
 * Uses the same systemd-logind low-level inhibitor mechanism as Ignore Lid:
 * https://github.com/mfloto/ignore-lid
 *
 * SPDX-License-Identifier: GPL-2.0-or-later
 */

import Gio from 'gi://Gio';
import GLib from 'gi://GLib';

const LogindInterface = `<node>
<interface name="org.freedesktop.login1.Manager">
    <method name="Inhibit">
        <arg type="s" name="what" direction="in"/>
        <arg type="s" name="who" direction="in"/>
        <arg type="s" name="why" direction="in"/>
        <arg type="s" name="mode" direction="in"/>
        <arg type="h" name="fd" direction="out"/>
    </method>
</interface>
</node>`;

const LogindProxy = Gio.DBusProxy.makeProxyWrapper(LogindInterface);

export class LidInhibitor {
    constructor() {
        this._active = false;
        this._destroyed = false;
        this._fd = null;
        this._requestPending = false;
        this._proxy = new LogindProxy(
            Gio.DBus.system,
            'org.freedesktop.login1',
            '/org/freedesktop/login1'
        );
    }

    setActive(active) {
        this._active = active;

        if (active) {
            this._acquire();
        } else {
            this._release();
        }
    }

    _acquire() {
        if (this._destroyed || this._fd !== null || this._requestPending) {
            return;
        }

        this._requestPending = true;
        this._proxy.InhibitRemote(
            'handle-lid-switch',
            'Caffeinate',
            'Caffeinate is active',
            'block',
            (result, error, fdList) => {
                this._requestPending = false;

                if (error) {
                    console.error(`[Caffeinate] Could not inhibit the lid switch: ${error.message}`);
                    return;
                }

                const [fdHandle] = result;
                const fd = fdList?.get(fdHandle);
                if (fd === undefined) {
                    console.error('[Caffeinate] logind returned no lid-switch inhibitor descriptor');
                    return;
                }

                if (this._destroyed || !this._active || this._fd !== null) {
                    GLib.close(fd);
                    return;
                }

                this._fd = fd;
            }
        );
    }

    _release() {
        if (this._fd === null) {
            return;
        }

        GLib.close(this._fd);
        this._fd = null;
    }

    destroy() {
        this._destroyed = true;
        this._active = false;
        this._release();
        this._proxy = null;
    }
}
