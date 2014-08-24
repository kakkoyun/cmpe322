package B;

import java.io.PrintWriter;
import java.net.Socket;

public class Client {
	String serverName;
	int port;
	String nickname;
	
	public Client(String serverName, int port, String nickname){
		this.serverName = serverName;
		this.port = port;
		this.nickname = nickname;
	}
	
	public void run() {
		try {
			Socket socket = new Socket(serverName, port);
			PrintWriter toServer = new PrintWriter(socket.getOutputStream());
			ClientListener cl = new ClientListener(socket);
			toServer.println("USERNAME: "+nickname);
			System.out.println("Hello "+nickname);
			toServer.flush();
			Thread t = new Thread(cl);
			t.start();
			System.out.println("USAGE:");
			System.out.println("'GETLIST' to get your messages.");
			System.out.println("'DELETE: <message_number>' to delete a message.");
			System.out.println("'SEND: <nickname> : <message>' to send a message.");
			while(true) {
				System.out.print(">>  ");
				String toSend = System.console().readLine();
				if (cl.isFinished) {
					break;
				}
				if (toSend != " "){
					System.out.println("Request sending to the server...");
					toServer.println(toSend);
					toServer.flush();
					System.out.println("sent message");
				}
			}
		} catch(Exception e){
			System.out.println("Something went wrong during the service.");
			System.out.println(e);
			e.printStackTrace();
		}
	}
}
