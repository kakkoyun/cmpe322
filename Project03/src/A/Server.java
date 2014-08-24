package A;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.util.HashMap;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class Server {

	private int port;
	HashMap<Integer,Integer> map = new HashMap<Integer,Integer>();
	
	public int getPort() {
		return port;
	}

	public void setPort(int port) {
		this.port = port;
	}
	
	public Server(int port){
		this.port = port;
	}
	
	public void run(){
		byte[] buffer = new byte[1500];
		DatagramPacket packet = new DatagramPacket(buffer, buffer.length);
		int poolSize=4;
		ExecutorService pool = Executors.newFixedThreadPool(poolSize);
		try{
			DatagramSocket serverSocket = new DatagramSocket(port);
			System.out.println("Server waiting!!");
			for(;;){
				serverSocket.receive(packet);
				String str = new String(packet.getData(), packet.getOffset(), packet.getLength());
				System.out.println("Received request from : "+ packet.getAddress() +"/"+ packet.getPort() +" : S"+ packet.getData());
				HashMapDictionary mapDealer = new HashMapDictionary(map, str, serverSocket, packet.getAddress(), packet.getPort());
				pool.submit(mapDealer);
			}
		} catch(IOException e){
			System.out.println(String.format("Error %s", e));
		}
		try {
			pool.shutdown();
			System.out.println("Awaiting for the thread pool to finish......");
			if (!pool.awaitTermination(60, TimeUnit.SECONDS)){
				System.err.println("Thread pool did not terminate in a fair time.");
			}
		} catch(InterruptedException e) {
			
		}
	}
}
