/* mxv.f -- translated by f2c (version 19980913).
   You must link the resulting object file with the libraries:
	-lf2c -lm   (in that order)
*/

#include "f2c.h"

/* $Procedure MXV ( Matrix times vector, 3x3 ) */
/* Subroutine */ int mxv_(doublereal *m, doublereal *vin, doublereal *vout)
{
    /* System generated locals */
    integer i__1, i__2, i__3, i__4;

    /* Builtin functions */
    integer s_rnge(char *, integer, char *, integer);

    /* Local variables */
    integer i__;
    doublereal prodv[3];

/* $ Abstract */

/*     Multiply a 3x3 double precision matrix with a 3-dimensional */
/*     double precision vector. */

/* $ Disclaimer */

/*     THIS SOFTWARE AND ANY RELATED MATERIALS WERE CREATED BY THE */
/*     CALIFORNIA INSTITUTE OF TECHNOLOGY (CALTECH) UNDER A U.S. */
/*     GOVERNMENT CONTRACT WITH THE NATIONAL AERONAUTICS AND SPACE */
/*     ADMINISTRATION (NASA). THE SOFTWARE IS TECHNOLOGY AND SOFTWARE */
/*     PUBLICLY AVAILABLE UNDER U.S. EXPORT LAWS AND IS PROVIDED "AS-IS" */
/*     TO THE RECIPIENT WITHOUT WARRANTY OF ANY KIND, INCLUDING ANY */
/*     WARRANTIES OF PERFORMANCE OR MERCHANTABILITY OR FITNESS FOR A */
/*     PARTICULAR USE OR PURPOSE (AS SET FORTH IN UNITED STATES UCC */
/*     SECTIONS 2312-2313) OR FOR ANY PURPOSE WHATSOEVER, FOR THE */
/*     SOFTWARE AND RELATED MATERIALS, HOWEVER USED. */

/*     IN NO EVENT SHALL CALTECH, ITS JET PROPULSION LABORATORY, OR NASA */
/*     BE LIABLE FOR ANY DAMAGES AND/OR COSTS, INCLUDING, BUT NOT */
/*     LIMITED TO, INCIDENTAL OR CONSEQUENTIAL DAMAGES OF ANY KIND, */
/*     INCLUDING ECONOMIC DAMAGE OR INJURY TO PROPERTY AND LOST PROFITS, */
/*     REGARDLESS OF WHETHER CALTECH, JPL, OR NASA BE ADVISED, HAVE */
/*     REASON TO KNOW, OR, IN FACT, SHALL KNOW OF THE POSSIBILITY. */

/*     RECIPIENT BEARS ALL RISK RELATING TO QUALITY AND PERFORMANCE OF */
/*     THE SOFTWARE AND ANY RELATED MATERIALS, AND AGREES TO INDEMNIFY */
/*     CALTECH AND NASA FOR ALL THIRD-PARTY CLAIMS RESULTING FROM THE */
/*     ACTIONS OF RECIPIENT IN THE USE OF THE SOFTWARE. */

/* $ Required_Reading */

/*     None. */

/* $ Keywords */

/*     MATRIX */
/*     VECTOR */

/* $ Declarations */
/* $ Brief_I/O */

/*     VARIABLE  I/O  DESCRIPTION */
/*     --------  ---  -------------------------------------------------- */
/*     M          I   3x3 double precision matrix. */
/*     VIN        I   3-dimensional double precision vector. */
/*     VOUT       O   3-dimensional double precision vector. VOUT is */
/*                    the product M*VIN. */

/* $ Detailed_Input */

/*     M        is an arbitrary 3x3 double precision matrix. */

/*     VIN      is an arbitrary 3-dimensional double precision vector. */

/* $ Detailed_Output */

/*     VOUT     is a 3-dimensional double precision vector. VOUT is */
/*              the product M * V. */

/* $ Parameters */

/*     None. */

/* $ Exceptions */

/*     Error free. */

/* $ Files */

/*     None. */

/* $ Particulars */

/*     The code reflects precisely the following mathematical expression */

/*        For each value of the subscript I from 1 to 3: */

/*                        3 */
/*                     .----- */
/*                      \ */
/*           VOUT(I) =   )  M(I,K) * VIN(K) */
/*                      / */
/*                     '----- */
/*                       K=1 */

/* $ Examples */

/*     The numerical results shown for this example may differ across */
/*     platforms. The results depend on the SPICE kernels used as */
/*     input, the compiler and supporting libraries, and the machine */
/*     specific arithmetic implementation. */

/*     1) Given a 3x3 matrix and a 3-vector, multiply the matrix by */
/*        the vector. */


/*        Example code begins here. */


/*              PROGRAM MXV_EX1 */
/*              IMPLICIT NONE */

/*        C */
/*        C     Local variables. */
/*        C */
/*              DOUBLE PRECISION      M    ( 3, 3 ) */
/*              DOUBLE PRECISION      VIN  ( 3    ) */
/*              DOUBLE PRECISION      VOUT ( 3    ) */

/*        C */
/*        C     Define M and VIN. */
/*        C */
/*              DATA                  M    /  0.0D0, -1.0D0,  0.0D0, */
/*             .                              1.0D0,  0.0D0,  0.0D0, */
/*             .                              0.0D0,  0.0D0,  1.0D0  / */

/*              DATA                  VIN  /  1.0D0,  2.0D0,  3.0D0  / */

/*        C */
/*        C     Multiply M by VIN. */
/*        C */
/*              CALL MXV ( M, VIN, VOUT ) */

/*              WRITE(*,'(A)') 'M times VIN:' */
/*              WRITE(*,'(3F10.3)') VOUT */

/*              END */


/*        When this program was executed on a Mac/Intel/gfortran/64-bit */
/*        platform, the output was: */


/*        M times VIN: */
/*             2.000    -1.000     3.000 */


/* $ Restrictions */

/*     1)  The user is responsible for checking the magnitudes of the */
/*         elements of M and VIN so that a floating point overflow does */
/*         not occur. */

/* $ Literature_References */

/*     None. */

/* $ Author_and_Institution */

/*     N.J. Bachman       (JPL) */
/*     J. Diaz del Rio    (ODC Space) */
/*     W.M. Owen          (JPL) */
/*     W.L. Taber         (JPL) */

/* $ Version */

/* -    SPICELIB Version 1.1.0, 13-AUG-2021 (JDR) */

/*        Edited the header to comply with NAIF standard. Added complete */
/*        code example based on the existing example. */

/*        Changed input argument name MATRIX to M for consistency with */
/*        other routines. */

/*        Added IMPLICIT NONE statement. */

/* -    SPICELIB Version 1.0.2, 22-APR-2010 (NJB) */

/*        Header correction: assertions that the output */
/*        can overwrite the input have been removed. */

/* -    SPICELIB Version 1.0.1, 10-MAR-1992 (WLT) */

/*        Comment section for permuted index source lines was added */
/*        following the header. */

/* -    SPICELIB Version 1.0.0, 31-JAN-1990 (WMO) */

/* -& */
/* $ Index_Entries */

/*     matrix times 3-dimensional vector */

/* -& */

/*     Local variables */


/*  Perform the matrix-vector multiplication */

    for (i__ = 1; i__ <= 3; ++i__) {
	prodv[(i__1 = i__ - 1) < 3 && 0 <= i__1 ? i__1 : s_rnge("prodv", i__1,
		 "mxv_", (ftnlen)211)] = m[(i__2 = i__ - 1) < 9 && 0 <= i__2 ?
		 i__2 : s_rnge("m", i__2, "mxv_", (ftnlen)211)] * vin[0] + m[(
		i__3 = i__ + 2) < 9 && 0 <= i__3 ? i__3 : s_rnge("m", i__3, 
		"mxv_", (ftnlen)211)] * vin[1] + m[(i__4 = i__ + 5) < 9 && 0 
		<= i__4 ? i__4 : s_rnge("m", i__4, "mxv_", (ftnlen)211)] * 
		vin[2];
    }

/*  Move the buffered vector into the output vector VOUT. */

    vout[0] = prodv[0];
    vout[1] = prodv[1];
    vout[2] = prodv[2];
    return 0;
} /* mxv_ */

