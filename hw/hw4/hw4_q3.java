// my attempt at writing this assignment in java instead...
import java.util.*;


public static void main(String[] args) {
	
	num_points = 100000	
	Scanner input = new Scanner("test_files/test0000_1549220786.7021272_N100000.txt")
	int[][] points = new int[num_points][2]

	// Run test 1: Naive
	final long startTime = System.currentTimeMillis();

	System.out.println("runtime naive: " + (System.currentTimeMillis() - startTime));

	// Run test 2: O(n log^2)
	startTime = System.currentTimeMillis();

	System.out.println("runtime O(n log^2): " + (System.currentTimeMillis() - startTime));

	// Run test 3: O(n log)
	startTime = System.currentTimeMillis();
	System.out.println("runtime O(n log): " + (System.currentTimeMillis() - startTime));




}



public static int naive() {



}
