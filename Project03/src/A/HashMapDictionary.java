package A;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.util.HashMap;

public class HashMapDictionary implements Runnable {
	
	HashMap<Integer,Integer> map;
	String message;
	DatagramSocket socket;
	InetAddress clientAddress;
	int clientPort;
	
	public HashMapDictionary(HashMap<Integer,Integer> map, String str, DatagramSocket serverSocket, InetAddress inetAddress, int port) {
		this.map = map;
		this.message = str;
		this.socket = serverSocket;
		this.clientAddress = inetAddress;
		this.clientPort = port;
	}
	
	public void addPair(int key, int value) {
		map.put(key, value);
	}
		
	public Integer retrieveValue(int key) {
		return map.get(key);
	}
	
	public Integer removePair(int key) {
		return map.remove(key);
	}

	@Override
	public void run() {
		String answer = "";
		String[] str = message.split(",");
		if (str.length<3){
			answer = "NOK: Not a valid command!";
		}
		else {
			String option = str[0];
			try {
				int key = Integer.parseInt(str[1]);
				int value = Integer.parseInt(str[2]);
				if (option.equals("ADD")){
					addPair(key, value);
					answer = "OK: Key value pair added successfully.";
				}
				else if (option.equals("REMOVE")){
					Integer val = removePair(key);
					if (val == null){
						answer = "NOK: Key value pair is not present on the map.";
					}
					else {
						answer = "OK: Key value pair removed successfully.";
					}
				}
				else if (option.equals("QUERY")){
					
					Integer newValue = retrieveValue(key);
					if (newValue == null){
						answer = "NOK: There is not a value for given key : "+key;
					}
					else {
						answer = "OK: The value of "+key+": "+newValue;
					}
				}
				else {
					answer = "NOK: Not a valid option!";
				}
			} catch(NumberFormatException e){
				answer = "OK: Key and value have to be integers";
			}
		}
		try {
			byte[] sendbuffer = answer.getBytes();
			DatagramPacket replyPacket = new DatagramPacket(sendbuffer, sendbuffer.length, clientAddress, clientPort);
			socket.send(replyPacket);
		} catch(Exception e) {
			System.out.println(String.format("Error %s", e));
		}
		
	}
}
