/*

-Procedure ckcls_c ( CK, Close file )

-Abstract

   Close an open CK file.

-Disclaimer

   THIS SOFTWARE AND ANY RELATED MATERIALS WERE CREATED BY THE
   CALIFORNIA INSTITUTE OF TECHNOLOGY (CALTECH) UNDER A U.S.
   GOVERNMENT CONTRACT WITH THE NATIONAL AERONAUTICS AND SPACE
   ADMINISTRATION (NASA). THE SOFTWARE IS TECHNOLOGY AND SOFTWARE
   PUBLICLY AVAILABLE UNDER U.S. EXPORT LAWS AND IS PROVIDED "AS-IS"
   TO THE RECIPIENT WITHOUT WARRANTY OF ANY KIND, INCLUDING ANY
   WARRANTIES OF PERFORMANCE OR MERCHANTABILITY OR FITNESS FOR A
   PARTICULAR USE OR PURPOSE (AS SET FORTH IN UNITED STATES UCC
   SECTIONS 2312-2313) OR FOR ANY PURPOSE WHATSOEVER, FOR THE
   SOFTWARE AND RELATED MATERIALS, HOWEVER USED.

   IN NO EVENT SHALL CALTECH, ITS JET PROPULSION LABORATORY, OR NASA
   BE LIABLE FOR ANY DAMAGES AND/OR COSTS, INCLUDING, BUT NOT
   LIMITED TO, INCIDENTAL OR CONSEQUENTIAL DAMAGES OF ANY KIND,
   INCLUDING ECONOMIC DAMAGE OR INJURY TO PROPERTY AND LOST PROFITS,
   REGARDLESS OF WHETHER CALTECH, JPL, OR NASA BE ADVISED, HAVE
   REASON TO KNOW, OR, IN FACT, SHALL KNOW OF THE POSSIBILITY.

   RECIPIENT BEARS ALL RISK RELATING TO QUALITY AND PERFORMANCE OF
   THE SOFTWARE AND ANY RELATED MATERIALS, AND AGREES TO INDEMNIFY
   CALTECH AND NASA FOR ALL THIRD-PARTY CLAIMS RESULTING FROM THE
   ACTIONS OF RECIPIENT IN THE USE OF THE SOFTWARE.

-Required_Reading

   None.

-Keywords

   CK

*/

   #include "SpiceUsr.h"
   #include "SpiceZfc.h"
   #include "SpiceZst.h"

   void ckcls_c ( SpiceInt handle )

/*

-Brief_I/O

   VARIABLE  I/O  DESCRIPTION
   --------  ---  --------------------------------------------------
   handle     I   Handle of the CK file to be closed.

-Detailed_Input

   handle      is the handle of the CK file that is to be closed.

-Detailed_Output

   None.

-Parameters

   None.

-Exceptions

   1)  If there are no segments in the file, the error
       SPICE(NOSEGMENTSFOUND) is signaled by a routine in the call tree of
       this routine.

-Files

   See -Detailed_Input.

-Particulars

   Close the CK file attached to handle.

-Examples

   The numerical results shown for this example may differ across
   platforms. The results depend on the SPICE kernels used as
   input, the compiler and supporting libraries, and the machine
   specific arithmetic implementation.

   1) Create a CK type 3 segment; fill with data for a simple time
      dependent rotation and angular velocity, and reserve room in
      the CK comments area for 5000 characters.

      Example code begins here.


      /.
         Program ckcls_ex1
      ./
      #include "SpiceUsr.h"

      int main( )
      {

         /.
         Local parameters.
         ./
         #define CK3          "ckcls_ex1.bc"
         #define SPTICK       0.001
         #define INST         -77703
         #define MAXREC       201

         /.
         Local variables.
         ./
         SpiceChar          * ref;
         SpiceChar          * ifname;
         SpiceChar          * segid;

         SpiceDouble          avvs   [MAXREC][3];
         SpiceDouble          begtim;
         SpiceDouble          endtim;
         SpiceDouble          quats  [MAXREC][4];
         SpiceDouble          rate;
         SpiceDouble          rwmat  [3][3];
         SpiceDouble          spaces;
         SpiceDouble          sclkdp [MAXREC];
         SpiceDouble          starts [MAXREC/2];
         SpiceDouble          sticks;
         SpiceDouble          theta;
         SpiceDouble          wmat   [3][3];
         SpiceDouble          wquat  [4];

         SpiceInt             handle;
         SpiceInt             i;
         SpiceInt             ncomch;
         SpiceInt             nints;

         SpiceBoolean         avflag;

         /.
         `ncomch' is the number of characters to reserve for the
         kernel's comment area. This example doesn't write
         comments, so set to zero.
         ./
         ncomch = 0;

         /.
         The base reference from for the rotation data.
         ./
         ref = "J2000";

         /.
         Time spacing in encoded ticks and in seconds
         ./
         sticks = 10.0;
         spaces = sticks * SPTICK;

         /.
         Declare an angular rate in radians per sec.
         ./
         rate = 1.e-2;

         /.
         Internal file name and segment ID.
         ./
         segid  = "Test type 3 CK segment";
         ifname = "Test CK type 3 segment created by ckw03_c";

         /.
         Open a new kernel.
         ./
         ckopn_c ( CK3, ifname, ncomch, &handle );

         /.
         Create a 3x3 double precision identity matrix.
         ./
         ident_c ( wmat );

         /.
         Convert the matrix to quaternion.
         ./
         m2q_c ( wmat, wquat );

         /.
         Copy the work quaternion to the first row of
         `quats'.
         ./
         moved_c ( wquat, 4, quats[0] );

         /.
         Create an angular velocity vector. This vector is in the
         `ref' reference frame and indicates a constant rotation
         about the Z axis.
         ./
         vpack_c ( 0.0, 0.0, rate, avvs[0] );

         /.
         Set the initial value of the encoded ticks.
         ./
         sclkdp[0] = 1000.0;

         /.
         Fill the rest of the `avvs' and `quats' matrices
         with simple data.
         ./
         for ( i = 1; i < MAXREC; i++ )
         {

            /.
            Create the corresponding encoded tick value in
            increments of `sticks' with an initial value of
            1000.0 ticks.
            ./
            sclkdp[i] = 1000.0 + i * sticks;

            /.
            Create the transformation matrix for a rotation of
            `theta' about the Z axis. Calculate `theta' from the
            constant angular rate `rate' at increments of `spaces'.
            ./
            theta = i * rate * spaces;
            rotmat_c ( wmat, theta, 3, rwmat );

            /.
            Convert the `rwmat' matrix to SPICE type quaternion.
            ./
            m2q_c ( rwmat, wquat );

            /.
            Store the quaternion in the `quats' matrix.
            Store angular velocity in `avvs'.
            ./
            moved_c ( wquat, 4, quats[i] );
            vpack_c ( 0.0, 0.0, rate, avvs[i] );

         }

         /.
         Create an array start times for the interpolation
         intervals. The end time for a particular interval is
         determined as the time of the final data value prior in
          time to the next start time.
         ./
         nints = MAXREC/2;
         for ( i = 0; i < nints; i++ )
         {

            starts[i] = sclkdp[i*2];

         }

         /.
         Set the segment boundaries equal to the first and last
         time for the data arrays.
         ./
         begtim = sclkdp[0];
         endtim = sclkdp[MAXREC-1];

         /.
         This segment contains angular velocity.
         ./
         avflag = SPICETRUE;

         /.
         All information ready to write. Write to a CK type 3
         segment to the file indicated by `handle'.
         ./
         ckw03_c ( handle, begtim, endtim, INST, ref,   avflag, segid,
                   MAXREC, sclkdp, quats,  avvs, nints, starts       );

         /.
         SAFELY close the file.
         ./
         ckcls_c ( handle );

         return ( 0 );
      }


      When this program is executed, no output is presented on
      screen. After run completion, a new CK file exists in the
      output directory.

-Restrictions

   None.

-Literature_References

   None.

-Author_and_Institution

   N.J. Bachman        (JPL)
   J. Diaz del Rio     (ODC Space)
   K.R. Gehringer      (JPL)
   E.D. Wright         (JPL)

-Version

   -CSPICE Version 1.0.2, 10-AUG-2021 (JDR)

       Updated the header to comply with NAIF standard. Added
       complete code example based on existing fragment.

       Re-ordered header sections.

   -CSPICE Version 1.0.1, 08-MAR-2002 (EDW)

       Corrected header typo. Examples" to -Examples.

   -CSPICE Version 1.0.0, 08-FEB-1998 (NJB) (KRG)

       Based on SPICELIB Version 1.0.0, 26-JAN-1995 (KRG)

-Index_Entries

   close a CK file

-&
*/

{ /* Begin ckcls_c */


   /*
   Participate in error handling.
   */
   chkin_c ( "ckcls_c");


   ckcls_ ( ( integer * ) &handle );


   chkout_c ( "ckcls_c");

} /* End ckcls_c */
