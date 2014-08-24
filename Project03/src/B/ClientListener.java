package B;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.Socket;

public class ClientListener implements Runnable{

	BufferedReader inReader;
	Socket socket;
	InputStream inStream;
	boolean isFinished=false;
	
	public ClientListener(Socket socket) {
		this.socket = socket;
		try {
			inStream = socket.getInputStream();
			inReader = new BufferedReader(new InputStreamReader(inStream));
		} catch (Exception e) {
			System.out.println("Something went wrong during client listener initialization.");
			System.out.println(e);
			e.printStackTrace();
		}
	}
	
	@Override
	public void run() {
		try {
			byte[] buf = new byte[1024];
			for(;;){
				int n = socket.getInputStream().read(buf);
				if (n<0) {
					System.out.println("Server terminated the connection.");
					break;
				}
				System.out.println(new String(buf, 0, n));
			}
		} catch (Exception e) {
			System.out.println("Something went wrong during the client listener loop:");
			System.out.println(e);
			e.printStackTrace();
		}
		isFinished = true;
	}

}
