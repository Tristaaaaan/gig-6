package org.test.app;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import java.util.ArrayList;
import java.util.List;

public class BluetoothScanner {
    private Context context;
    private BluetoothAdapter bluetoothAdapter;
    private List<String> devicesList;

    public BluetoothScanner(Context context) {
        this.context = context;
        bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
        devicesList = new ArrayList<>();

        // Register a BroadcastReceiver to receive Bluetooth device discovery results.
        IntentFilter filter = new IntentFilter(BluetoothDevice.ACTION_FOUND);
        context.registerReceiver(receiver, filter);
    }

    public List<String> scanDevices() {
        devicesList.clear();
        if (bluetoothAdapter != null && bluetoothAdapter.isEnabled()) {
            bluetoothAdapter.startDiscovery();
        }
        return devicesList;
    }

    private final BroadcastReceiver receiver = new BroadcastReceiver() {
        public void onReceive(Context context, Intent intent) {
            String action = intent.getAction();
            if (BluetoothDevice.ACTION_FOUND.equals(action)) {
                BluetoothDevice device = intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE);
                if (device != null) {
                    String deviceName = device.getName();
                    String deviceAddress = device.getAddress();
                    devicesList.add(deviceName + " (" + deviceAddress + ")");
                }
            }
        }
    };
}
