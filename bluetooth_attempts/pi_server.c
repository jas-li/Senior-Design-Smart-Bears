#include <stdio.h>
#include <unistd.h>
#include <sys/socket.h>
#include <bluetooth/bluetooth.h>
#include <bluetooth/rfcomm.h>

int main() {
    struct sockaddr_rc loc_addr = {0}, rem_addr = {0};
    char buf[1024] = {0};
    int sock, client, bytes_read;
    socklen_t opt = sizeof(rem_addr);

    // Create RFCOMM socket
    sock = socket(AF_BLUETOOTH, SOCK_STREAM, BTPROTO_RFCOMM);
    
    // Bind to channel 1
    loc_addr.rc_family = AF_BLUETOOTH;
    loc_addr.rc_bdaddr = *BDADDR_ANY;
    loc_addr.rc_channel = 1;
    bind(sock, (struct sockaddr *)&loc_addr, sizeof(loc_addr));

    listen(sock, 1);
    printf("Waiting for ESP32 connection on channel 1...\n");

    // Accept connection
    client = accept(sock, (struct sockaddr *)&rem_addr, &opt);
    ba2str(&rem_addr.rc_bdaddr, buf);
    printf("Connected to %s\n", buf);

    while(1) {
        bytes_read = read(client, buf, sizeof(buf));
        if(bytes_read > 0) {
            printf("Received: %s", buf);
            write(client, buf, bytes_read); // Echo back
        }
    }

    close(client);
    close(sock);
    return 0;
}
