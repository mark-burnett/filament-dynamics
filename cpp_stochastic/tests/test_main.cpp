/* Generic main for running gtest test cases.
 *
 * Mark Burnett, November 2008
 */

#include <gtest/gtest.h>

int main(int argc, char *argv[]) {

    // Initialize Test environment
    testing::InitGoogleTest( &argc, argv );

    // Run tests
    return RUN_ALL_TESTS();
}
