package A;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.util.Random;

public class Client extends Thread {
	String serverName;
	int port;

	public Client(String serverName, int port){
		this.serverName = serverName;
		this.port = port;
	}

	public void run(){
		try {
			DatagramSocket clientSocket = new DatagramSocket();
			InetAddress srvAddress = InetAddress.getByName(serverName);
			DatagramPacket packet, receivePacket;
			byte[] receiveBuffer = new byte[1500];
			Random random = new Random();
			String[] options = {"ADD", "QUERY", "REMOVE"};
			for(;;){
				// create a random message
				Integer key = random.nextInt(100);
				Integer value = random.nextInt(5000);
				Integer optionIndex = random.nextInt(3);
				String randomOption = options[optionIndex];
				String message = randomOption+","+key+","+value;
				byte[] sendbuffer = message.getBytes();
				System.out.println("Sending messsage: " + message);

				packet = new DatagramPacket(sendbuffer, sendbuffer.length, srvAddress, port);
				clientSocket.send(packet);

				receivePacket = new DatagramPacket(receiveBuffer, receiveBuffer.length);
				clientSocket.receive(receivePacket);

				System.out.println("Received message from server : "+ new String(receivePacket.getData(), receivePacket.getOffset(), receivePacket.getLength()));
				sleep(300);
			}
		} catch(Exception e) {
				System.out.println(String.format("Error %s", e));
			}
	}
}
