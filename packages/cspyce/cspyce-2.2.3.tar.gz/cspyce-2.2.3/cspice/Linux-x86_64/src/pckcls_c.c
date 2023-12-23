/*

-Procedure pckcls_c ( PCK, close file )

-Abstract

   Close an open PCK file.

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

   PCK

-Keywords

   PCK

*/

   #include "SpiceUsr.h"
   #include "SpiceZfc.h"
   #include "SpiceZst.h"

   void pckcls_c ( SpiceInt handle )

/*

-Brief_I/O

   VARIABLE  I/O  DESCRIPTION
   --------  ---  --------------------------------------------------
   handle     I   Handle of the PCK file to be closed.

-Detailed_Input

   handle      is the handle of the PCK file that is to be closed.

-Detailed_Output

   None.

-Parameters

   None.

-Exceptions

   1)  If there are no segments in the file, the error
       SPICE(NOSEGMENTSFOUND) is signaled by a routine in the call
       tree of this routine.

-Files

   See argument `handle'.

-Particulars

   None.

-Examples

   The numerical results shown for this example may differ across
   platforms. The results depend on the SPICE kernels used as
   input, the compiler and supporting libraries, and the machine
   specific arithmetic implementation.

   1) Suppose that you have sets of Chebyshev polynomial
      coefficients in an array pertaining to the orientation of
      the Moon body-fixed frame with the frame class ID 301
      relative to the J2000 reference frame, and want
      to put these into a type 2 segment PCK file. The following
      example could be used to add one new type 2 segment. To add
      multiple segments, put the call to pckw02_c in a loop.


      Example code begins here.


      /.
         Program pckcls_ex1
      ./
      #include "SpiceUsr.h"

      int main( )
      {

         /.
         Local parameters
         ./
         #define FNAME        "pckcls_ex1.bpc"
         #define BODY         301
         #define POLYDG       9
         #define SZCDAT       60

         /.
         Local variables
         ./
         SpiceChar          * ifname;
         SpiceChar          * segid;

         SpiceDouble          btime;
         SpiceDouble          first;
         SpiceDouble          intlen;
         SpiceDouble          last;

         SpiceInt             handle;
         SpiceInt             n;
         SpiceInt             nresvc;

         /.
         Set the input data: RA/DEC/W coefficients,
         begin time for the first record, start/end times
         for the segment, length of the time covered by
         each record, and number of logical records.

         `cdata' contains the ra/dec/w coefficients: first the
         the polydeg + 1 for the RA first record, then the
         polydeg + 1 for the DEC first record, then the
         polydeg +1 for W first record, then the polydeg + 1
         for the RA second record, and so on.
         ./
         SpiceDouble          cdata  [SZCDAT] = {
                       -5.4242086033301107e-002, -5.2241405162792561e-005,
                        8.9751456289930307e-005, -1.5288696963234620e-005,
                        1.3218870864581395e-006,  5.9822156790328180e-007,
                       -6.5967702052551211e-008, -9.9084309118396298e-009,
                        4.9276055963541578e-010,  1.1612267413829385e-010,
                        0.42498898565916610,      1.3999219324235620e-004,
                       -1.8855140511098865e-005, -2.1964684808526649e-006,
                        1.4229817868138752e-006, -1.6991716166847001e-007,
                       -3.4824688140649506e-008,  2.9208428745895990e-009,
                        4.4217757657060300e-010, -3.9211207055305402e-012,
                        2565.0633504619473,       0.92003769451305328,
                       -8.0503797901914501e-005,  1.1960860244433900e-005,
                       -1.2237900518372542e-006, -5.3651349407824562e-007,
                        6.0843372260403005e-008,  9.0211287487688797e-009,
                       -4.6460429330339309e-010, -1.0446918704281774e-010,
                       -5.3839796353225056e-002,  4.3378021974424991e-004,
                        4.8130091384819459e-005, -1.2283066272873327e-005,
                       -5.4099296265403208e-006, -4.4237368347319652e-007,
                        1.3004982445546169e-007,  1.9017128275284284e-008,
                       -7.0368223839477803e-011, -1.7119414526133175e-010,
                        0.42507987850614548,     -7.1844899448557937e-005,
                       -5.1052122872412865e-005, -8.9810401387721321e-006,
                       -1.4611718567948972e-007,  4.0883847771062547e-007,
                        4.6812854485029333e-008, -4.5698075960784951e-009,
                       -9.8679875320349531e-010, -7.9392503778178240e-011,
                        2566.9029069934054,       0.91952244801740568,
                       -6.0426151041179828e-005,  1.0850559330577959e-005,
                        5.1756033678137497e-006,  4.2127585555214782e-007,
                       -1.1774737441872970e-007, -1.7397191490163833e-008,
                        5.8908810244396165e-012,  1.4594279337955166e-010 };

         first  =   -43200.0;
         last   =  1339200.0;
         btime  =  first;
         intlen =   691200.0;
         n      =  2;

         /.
         Open a new PCK file.  For simplicity, we will not
         reserve any space for the comment area, so the
         number of reserved comment characters is zero.
         The variable `ifname' is the internal file name.
         ./
         nresvc  =  0;
         ifname  =  "Test PCK/Created 04-SEP-2019";

         pckopn_c ( FNAME, ifname, nresvc, &handle );

         /.
         Create a segment identifier.
         ./
         segid = "MY_SAMPLE_PCK_TYPE_2_SEGMENT";

         /.
         Write the segment.
         ./
         pckw02_c ( handle, BODY, "J2000", first, last, segid,
                    intlen, n,    POLYDG,  cdata, btime       );

         /.
         Close the file.
         ./
         pckcls_c ( handle );

         return ( 0 );
      }


      When this program is executed, no output is presented on
      screen. After run completion, a new PCK type 2 exists in
      the output directory.

-Restrictions

   None.

-Literature_References

   None.

-Author_and_Institution

   N.J. Bachman        (JPL)
   J. Diaz del Rio     (ODC Space)
   K.R. Gehringer      (JPL)

-Version

   -CSPICE Version 1.0.1, 04-AUG-2021 (JDR)

       Edited the header to comply with NAIF standard. Added
       complete code examples based on existing fragment.

   -CSPICE Version 1.0.0, 16-DEC-2016 (NJB) (KRG)

-Index_Entries

   close a PCK file

-&
*/

{ /* Begin pckcls_c */


   /*
   Participate in error tracing.
   */
   chkin_c ( "pckcls_c" );


   pckcls_ ( (integer *) &handle );


   chkout_c ( "pckcls_c" );

} /* End pckcls_c */
