package _2019.day01;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class Main {

	public static void main(String[] args) {
		Scanner scanner;
		String filename = "./src/_2019/day01/input";
		int sum1 = 0;
		int sum2 = 0;

		// Load file using scanner
		try {
			scanner = new Scanner(new File(filename));
			while (scanner.hasNextLine()) {
				int value = Integer.parseInt(scanner.nextLine());
				int result1 = calculFuel(value);
				int result2 = calculFuelAdded(result1, 0);

				sum1 += result1;
				sum2 += result2;
				System.out.println(value + " -> " + result1 + "/" + result2);
			}
			scanner.close();
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}

		System.out.println("Part 1: " + sum1);
		System.out.println("Part 2: " + (sum1 + sum2));
	}

	private static int calculFuel(int line) {
		//System.out.println(line);
		return Math.round(line / 3) - 2;
	}

	private static int calculFuelAdded(int fuel, int sum) {
		int f = calculFuel(fuel);
		if (f <= 0) {
			return sum;
		}
		return calculFuelAdded(f, sum + f);
	}

}
