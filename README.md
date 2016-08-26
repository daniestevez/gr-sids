# gr-sids
gr-sids is a set of GNUradio blocks designed to submit telemetry to a
server using the Simple Downlink Share Convention (SiDS) protocol. This is the
same protocol that it is used by the DK3WN Telemetry Forwarder
http://www.pe0sat.vgnet.nl/decoding/tlm-decoding-software/dk3wn/
These blocks can be used to sumbit telemetry to the PE0SAT Telemetry Server
http://tlm.pe0sat.nl/
or any other server implementing the SiDS protocol.

Currently there are two forwarder blocks, the **realtime** block and the
**recording** block.

The **realtime** block is used to submit telemetry as it is being received in
real time. It will take the packet timestamps from your system clock, so you
must ensure that it is accurate.

The **recording** block is used to submit telemetry from a recording that is
processed at any moment after it was made. You need to know the date and time at
which the recorded started. You also need to play back the recording at 1x
(realtime) speed. For this, you will usually need to put a Throttle block with a
rate equal to the sample rate of the recording. The telemetry forwarder is then
able to calculate the correct timestamps for the packets by taking into account
the elapsed time that the GNUradio flowgraph has being running and the timestamp
for the recording start (which you have to provide).

You need to provide the following parameters to the telemetry forwarder blocks:

  * URL. This is the submit URL of the telemetry server you are using.
  * NORAD ID. The NORAD ID of the satellite you are tracking. You can search the
    correct ID in http://celestrak.com/satcat/search.asp
  * Receiver callsign. This is your callsign.
  * Latitude and longitude. This are the coordinates of the groundstation. The
    format is as in 41.82748 or -23.84850. Positive coordinates are North or
    East. Negative coordinates are South or West.

For the **recording** block you also have to provide the start of the recording
in UTC. The format is YYYY-MM-DD HH:MM:SS.


