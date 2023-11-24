package _2019.day02;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Scanner;

public class Main {

	public static void main(String[] args) {
		Scanner scanner;
		String filename = "./src/_2019/day02/input";
		ArrayList<Integer> list = new ArrayList<>();

		// Load file using scanner
		try {
			scanner = new Scanner(new File(filename));
			while (scanner.hasNext()) {
				if (scanner.hasNextInt()) {
					list.add(scanner.nextInt());
				} else {
					System.out.println("nn");
				}
			}
		} catch (IOException e) {
			e.printStackTrace();
		}

		list.set(1, 12);
		list.set(2, 2);

		int value = 0;
		int cursor = 0;
		int in1, in2, out;
		while (value != 99) {
			value = list.get(cursor);
			in1 = list.get(cursor + 1);
			in2 = list.get(cursor + 2);
			out = list.get(cursor + 3);
			switch (value) {
				case 1:
					list.set(out, list.get(in1) + list.get(in2));
					break;
				case 2:
					list.set(out, list.get(in1) * list.get(in2));
					break;
				default:
					break;
			}
			cursor += 4;
		}

		System.out.println("Part 1: " + list.get(0));
		System.out.println("Part 1: " + (60 * 100 + 86));
	}

}
