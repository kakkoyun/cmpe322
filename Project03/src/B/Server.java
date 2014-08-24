package B;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.SelectionKey;
import java.nio.channels.Selector;
import java.nio.channels.ServerSocketChannel;
import java.nio.channels.SocketChannel;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;
import java.util.Map.Entry;

public class Server {
	private int port;
	private HashMap<String, SocketChannel> clients;
	private HashMap<SocketChannel, Inbox> inboxes;
	
	public int getPort() {
		return port;
	}

	public void setPort(int port) {
		this.port = port;
	}
	
	public Server(int port){
		this.port = port;
		this.clients = new HashMap<String, SocketChannel>();
		this.inboxes = new HashMap<SocketChannel, Inbox>();
	}
	
	void service(SelectionKey key){
		SocketChannel socketChannel = (SocketChannel)key.channel();
		ByteBuffer buf = ByteBuffer.allocate(1024);
		
		try {
			int n = socketChannel.read(buf);
			if (n>0){
				byte[] data = new byte[n];
				System.arraycopy(buf.array(), 0, data, 0, n);
				String message = new String(data);
				String[] commands = message.split(":");
				String answer = new String();
				if (commands.length == 1) {
					if (commands[0].trim().equals("GETLIST")) {
						answer = getlist(socketChannel);
					}
					else {
						answer = "Illegal command!";
					}
				}
				else if (commands.length == 2) {
					if (commands[0].trim().equals("DELETE")) {
						answer = deleteMessage(commands[1].trim(), socketChannel);
					}
					else if (commands[0].trim().equals("USERNAME")) {
						clients.put(commands[1].trim(), socketChannel);
						inboxes.put(socketChannel, new Inbox());
					}
					else {
						answer = "Illegal command!";
					}
				}
				else if (commands.length == 3) {
					if (commands[0].trim().equals("SEND")) {
						answer = sendMessage(commands[1].trim(), commands[2].trim(), socketChannel);
					}
					else {
						answer = "Illegal command!";
					}
				}
				else {
					answer = "Illegal command!";
				}
				socketChannel.write(ByteBuffer.wrap(answer.getBytes()));

			}
			else {
				System.out.println("Client disconnected.");
				clients.remove(socketChannel);
				key.cancel();
			}
		} catch(IOException e) {
			key.cancel();
			System.out.println("Client disconnected because of I/O exception.");
			System.out.println(e);
			e.printStackTrace();
		} catch(Exception e) {
			System.out.println("Something went wrong during the service.");
			System.out.println(e);
			e.printStackTrace();
		}
	}
	
	private String deleteMessage(String string, SocketChannel client) {
		try {
			Integer messageNum = Integer.parseInt(string);
			Inbox clientInbox = inboxes.get(client);
			String result = clientInbox.remove(messageNum);
			if (result == null) {
				return "There is not a message in your inbox numbered : "+messageNum;
			}
			else {
				return "Message deleted.";
			}
		} catch(NumberFormatException e) {
			return "Please give a message number!!!";
		}
		
	}

	private String sendMessage(String person, String message, SocketChannel client) {
		SocketChannel receiver = clients.get(person);
		String senderNick = new String();
		Iterator<Entry<String, SocketChannel>> it = clients.entrySet().iterator();
		System.out.println("sending");
	    while (it.hasNext()) {
	        Map.Entry<String, SocketChannel> pairs = (Map.Entry<String, SocketChannel>)it.next();
	        if (pairs.getValue().equals(client)){
	        	senderNick = pairs.getKey();
	        	break;
	        }
	        it.remove();
	    }
		if (receiver != null) {
			inboxes.get(receiver).add(senderNick+": "+message);
			return "Message sent.";
		}
		else {
			return "This person is not in chat application.";
		}
	}

	private String getlist(SocketChannel client) {
		return inboxes.get(client).getAll();
	}

	public void run() {
		try {
			Selector selector = Selector.open();
			ServerSocketChannel server = ServerSocketChannel.open();
			server.configureBlocking(false);
			InetSocketAddress socketAddress = new InetSocketAddress("", port);
			server.socket().bind(socketAddress);
			System.out.println("Accepting Clients...");
			SelectionKey acceptKey = server.register(selector, SelectionKey.OP_ACCEPT);
			while(acceptKey.selector().select()>0){
				Set<SelectionKey> readyKey = selector.selectedKeys();
				Iterator<SelectionKey> it = readyKey.iterator();
				while(it.hasNext()) {
					SelectionKey key = (SelectionKey)it.next();
					it.remove();
					if (! key.isValid()) {
						continue;
					}
					if (key.isAcceptable()) {
						System.out.println("Client accepted.");
						ServerSocketChannel ssc = (ServerSocketChannel)key.channel();
						SocketChannel clientSocket = (SocketChannel)ssc.accept();
						clientSocket.configureBlocking(false);
						SelectionKey another = clientSocket.register(selector, SelectionKey.OP_READ);
					}
					if (key.isReadable()) {
						service(key);
					}
				}
			}
		} catch(Exception e){
			System.out.println("Something went wrong!");
			System.out.println(e);
			e.printStackTrace();
		}
	}
}
