/*
 * camctrl.c provides control interface for Sony Imager
 *
 * Author: Aman Kansal, UCLA. July 2004.
 */


#include <stdio.h>
#include <errno.h>

#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#define closesocket(s) close(s)

#define HTTP_PORT 80
#define IP_FILE "/etc/ee209s_camip"	/* file containing camera IP address */

/*
 * converts pan and tilt values into a message accepted by the camera
 */
char *pantiltformat (char *buf, char *ipaddress,
		     int pan_actual_angle, int tilt_actual_angle, int zoom);

/*
 * converts zoom value into a message accepted by the camera
 */
char *zoomformat (char *buf, char *ipaddress, int zoom);


int
main (int argc, char **argv)
{
	struct sockaddr_in server;
	char address_str[16];
	unsigned long address_num;

	int sock;
	char buffer[81920];
	char command[256];
	int count, i, pan, zoom, tilt;

	struct in_addr camera_address;
	int inet_err;
	FILE *received;		/* stores data received over socket */

	if (argc == 5)
	  {
	          sprintf(address_str, "%s", argv[1]);
		  pan = atoi (argv[2]);
		  tilt = atoi (argv[3]);
		  zoom = atoi (argv[4]);
	  }
	else
	  {
		  fprintf (stderr,
			   "usage-  [ip pan_value tilt_value zoom_value]\n");
		  fprintf (stderr, "example:\n");
		  fprintf (stderr, "%s 192.168.0.100 25 10 + \n", argv[0]);
		  fprintf (stderr, " -170 < pan_value < 170\n");
		  fprintf (stderr, ", -20 < tilt_value < 90\n");
		  fprintf (stderr, "    0< zoom_value < 100\n");
		  exit (1);
	  }
	/* create socket */
	sock = socket (PF_INET, SOCK_STREAM, 0);
	if (sock < 0)
	  {
		  perror ("failed to create socket");
		  exit (1);
	  }

	printf ("Camera address: %s \n", address_str);


	/* set up camera address for socket connection */
	inet_err = inet_aton (address_str, &camera_address);
	if (inet_err = 0)
	  {
		  perror ("failed to convert address");
		  exit (1);
	  }

	server.sin_addr = camera_address;
	server.sin_family = AF_INET;
	server.sin_port = htons (HTTP_PORT);

	/* connect to the camera, commands will be sent over this socket */
	if (connect (sock, (struct sockaddr *) &server, sizeof (server)) < 0)
	  {
		  perror ("can't connect to camera");
		  exit (1);
	  }

	/* convert pan and tilt values to the command packet required by camera */
	pantiltformat (buffer, address_str, pan, tilt, zoom);
	/* send the pan/tilt command to camera */
	send (sock, buffer, strlen (buffer), 0);

	/* receive reply from camera */
	received = fopen ("communication_log.txt", "w");
	do
	  {
		  count = recv (sock, buffer, sizeof (buffer), 0);
		  for (i = 0; i < count; i++)
			  fprintf (received, "%c", buffer[i]);
		  /*  printf("%c",buffer[i]); */
	  }
	while ((count > 0) && (count < 60));
	fprintf (stdout, "\n");

	/* convert zoom value to the command packet required by the camera */
	zoomformat (buffer, address_str, zoom);
	/* send the zoom command to the camera */
	send (sock, buffer, strlen (buffer), 0);

	/* receive reply from camera */
	received = fopen ("communication_log.txt", "w");
	do
	  {
		  count = recv (sock, buffer, sizeof (buffer), 0);
		  for (i = 0; i < count; i++)
			  fprintf (received, "%c", buffer[i]);
		  /*    printf("%c",buffer[i]); */
	  }
	while ((count > 0) && (count < 60));
//    fprintf(stdout,"\n");

	/* get the image */
	/*sprintf (command,
		 "wget -q http://%s/oneshotimage.jpg 2>image_capture_error.log",
		 address_str);
	system (command);
	*/
	/* close the connection to the server */
	closesocket (sock);
	return count;
}

/* Function to convert pan and tilt values to SNC-RZ30N packet format */
char *
pantiltformat (char *buf,
	       char *ipaddress,
	       int pan_actual_angle, int tilt_actual_angle, int zoom)
{
	/* function to format a string buffer to make the VISCA PTZ command */
	char *pan_hexstr, *pan_comstr;
	char *tilt_hexstr, *tilt_comstr;
	char zomm_direct[9];
	int i;
	int pan_cam_dec, tilt_cam_dec;
	/* range checking on inut pan/tilt values */
	if (pan_actual_angle > 170)
		pan_actual_angle = 170;
	if (pan_actual_angle < -170)
		pan_actual_angle = -170;
	if (tilt_actual_angle < -25)
		tilt_actual_angle = -25;
	if (tilt_actual_angle > 90)
		tilt_actual_angle = 90;

	/* convert pan and tilt values to relevant byte characters

	   /*       Convert pan
	   *        degree changes:
	   *
	   *        ORIENTATION   ACTUAL_ANGLE CAM_ANGLE CAM_DEC CAM_HEX
	   *        Clockwise side:
	   *        forward         0            0        0      0000
	   *        max clkws       170          170      2448   0990
	   *        Counterclockwise side:
	   *        max ctrclk     -170          4381     63088  F670
	   *        forward         360          4551     65535  FFFF
	 */

	/* convert from actual angle to camera step (in decimal) */
	if (pan_actual_angle >= 0)
		pan_cam_dec = 14.4 * pan_actual_angle;
	else
		pan_cam_dec = 14.4 * (4551 + pan_actual_angle);

	/* convert pan steps from decimal to hex string */
	asprintf (&pan_hexstr, "%04x\0", pan_cam_dec);
	/* put in format 0y0y0y0y (where yyyy is the steps in hex) */
	asprintf (&pan_comstr, "0%c0%c0%c0%c\0",
		  pan_hexstr[0], pan_hexstr[1], pan_hexstr[2], pan_hexstr[3]);

	printf ("pan angle: %d\n", pan_actual_angle);
/*  printf("pan dec:%d\n", pan_cam_dec);
    printf("pan hexstr: %s\n", pan_hexstr);
    printf("pan comstr: %s\n", pan_comstr);
    printf("pan hexstr[0]: %c\n", pan_hexstr[0]);
*/


	/* Convert tilt
	 * degree changes:
	 *   ORIENTATION   ACTUAL_ANGLE CAM_ANGLE CAM_DEC CAM_HEX
	 *    Below 32.5:
	 *    level           0            4518.54  65066  FE2A
	 *    32.5            32.5         4551     65535  FFFF
	 *
	 *    Above 32.5:
	 *    32.5            32.5         0        0      0000
	 *    straight up     90           67.5     972    03CC
	 */

	/* convert from actual angle to camera step (in decimal) */
	if (tilt_actual_angle >= 32.5)
		tilt_cam_dec = 14.4 * (tilt_actual_angle - 32.5);
	else
		tilt_cam_dec = 14.4 * (4551 + (tilt_actual_angle - 32.5));

	/* convert pan steps from decimal to hex string */
	asprintf (&tilt_hexstr, "%04x\0", tilt_cam_dec);

	/* put in format 0y0y0y0y (where yyyy is the steps in hex) */
	asprintf (&tilt_comstr, "0%c0%c0%c0%c\0",
		  tilt_hexstr[0],
		  tilt_hexstr[1], tilt_hexstr[2], tilt_hexstr[3]);

	printf ("tilt angle: %d\n", tilt_actual_angle);
/*  printf("tilt dec:%d\n", tilt_cam_dec);
    printf("tilt hexstr: %s\n", tilt_hexstr);
    printf("tilt comstr: %s\n", tilt_comstr);
    printf("tilt hexstr[0]: %c\n", tilt_hexstr[0]);
*/

	sprintf (buf,
		 "GET /command/ptzf.cgi?VISCA=810106021010%s%sff HTTP/1.1\r\nHost:%s\n\n",
		 pan_comstr, tilt_comstr, ipaddress);
	return buf;
}

    /* function to format a string buffer to make the VISCA  
     * direct CAM_Zoom command
     */

char *
zoomformat (char *buf, char *ipaddress, int zoom)
{
	int zoom_scaled;
	char *zoom_hexstr;
	char *zoom_comstr;

	/* we get the zoom argument as a value between 0 and 100, which corresponds
	 * to HEX 0 to HEX 4000. (decimal 0 to decimal 16384)
	 */
	zoom_scaled = (zoom * 16384) / 100;

	/* convert pan steps from decimal to hex string */
	asprintf (&zoom_hexstr, "%04x\0", zoom_scaled);

	/* put in format 0y0y0y0y (where yyyy is the steps in hex) */
	asprintf (&zoom_comstr, "0%c0%c0%c0%c\0",
		  zoom_hexstr[0],
		  zoom_hexstr[1], zoom_hexstr[2], zoom_hexstr[3]);

	printf ("zoom: %d\n", zoom);
/*  printf("zoom scaled:%d\n", zoom_scaled);
    printf("zoom hexstr: %s\n", zoom_hexstr);
    printf("zoom comstr: %s\n", zoom_comstr);
*/

	sprintf (buf,
		 "GET /command/ptzf.cgi?VISCA=81010447%sff HTTP/1.1\r\nHost:%s\n\n",
		 zoom_comstr, ipaddress);
	return buf;
}
